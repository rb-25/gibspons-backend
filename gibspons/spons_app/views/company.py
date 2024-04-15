from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from spons_app.models import Company, Sponsorship
from spons_app.serializers import CompanySerializer, SponsorshipSerializer

from spons_app.customs.permissions import IsCompanyCreator,IsApproved
from spons_app.customs.pagination import CustomPagination


class CreateDisplayCompanyView(APIView):
    
    """View to create and display companies for an organisation"""
    
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name", "status","updated_at","user_id__username"]
    search_fields = ["name","user_id__username","status"]
    ordering_fields = ["name","status"]
    ordering = ["name"]
    
    def get(self,request):
        
        organisation_id = request.query_params.get('org')
        if organisation_id is None:
            return Response({'detail': 'Organization ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        companies = Company.objects.filter(organisation=organisation_id)
        
        if not companies:
            return Response({'detail': 'No companies found for the given organization ID'}, status=status.HTTP_404_NOT_FOUND)
        
        #queryset = SearchFilter.filter_queryset(request, companies,queryset, view=self)
        company_serializer = CompanySerializer(companies, many=True)
        return Response(company_serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        
        """This method creates a company and a sponsorship for the company."""
        
        curr_user = request.user
        current_organization_id = curr_user.organisation
               
        name = request.data.get('name')
        website = request.data.get('website')
        existing_company = Company.objects.filter(name=name, website=website).first()

        if not existing_company:
            company_serializer = CompanySerializer(data=request.data)
            company_serializer.is_valid(raise_exception=True)
            print("exists")
            company = company_serializer.save(organisation=current_organization_id)
        else:
            company = existing_company
            company_serializer = CompanySerializer(company)

        sponsorship_data = {
            'company': company.id,
            'event': request.data.get('event_id'),
            'contacted_by':request.user.id,
            'status': 'Not Contacted' 
        }
        sponsorship_serializer = SponsorshipSerializer(data=sponsorship_data)
        sponsorship_serializer.is_valid(raise_exception=True)
        sponsorship_serializer.save()
        
        return Response({
            'company': company_serializer.data,
            'sponsorship': sponsorship_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    
class UpdateDeleteCompanyView(APIView):
    
    """View to update and delete a company."""
    
    permission_classes=[IsAuthenticated,IsCompanyCreator,IsApproved]
    authentication_classes=[JWTAuthentication]
        
    @staticmethod
    def patch(request,company_id):
        company=get_object_or_404(Company,id=company_id)
        serializer=CompanySerializer(company,data=request.data,partial=True)    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def delete(request, company_id):
        company_to_delete=get_object_or_404(Company,id=company_id)
        company_to_delete.delete()
        return Response({'message': 'Company deleted successfully'}, status=status.HTTP_200_OK)

