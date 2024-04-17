from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from users.models import User,Organisation
from spons_app.models import Event,Company, POC, Sponsorship
from users.serializers import OrganisationSerializer
from spons_app.serializers import POCSerializer, CompanySerializer, EventSerializer, SponsorshipSerializer, POCCompanySerializer
from spons_app.customs.permissions import IsCompanyCreator, IsPOCCreater,IsApproved,IsAdmin
from spons_app.customs.pagination import CustomPagination


class CreateDisplayPOCView(APIView):
    
    """View to create and display POCs for a company"""
    
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name","company","email","linkedin","phone","user"]
    search_fields = ["name","company","email","linkedin","phone","user"]
    ordering_fields = ["name","company","user"]
    ordering = ["company"]
    
    def post(self,request):
        poc_data_list = request.data
        poc_objects = []

        for poc_data in poc_data_list:
            serializer = POCSerializer(data=poc_data)
            if serializer.is_valid():      
                serializer.save()
                poc_objects.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(poc_objects, status=status.HTTP_201_CREATED)
    
    @staticmethod    
    def get(request):
        company_id = request.query_params.get('company')
        if company_id is None:
            return Response({'detail': 'Company ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        poc = POC.objects.filter(company=company_id)
        if not poc:
            return Response({'detail': 'No POC found for the given Company ID'}, status=status.HTTP_404_NOT_FOUND)
        poc_serializer = POCSerializer(poc, many=True)
        return Response(poc_serializer.data, status=status.HTTP_200_OK)

class UpdateDeletePOCView(APIView):
    
    """View to update and delete POCs for a company"""
    
    permission_classes=[IsAuthenticated,IsPOCCreater,IsApproved]
    authentication_classes=[JWTAuthentication]
    
    @staticmethod
    def patch(request,POC_id):
        poc=get_object_or_404(POC,id=POC_id)
        serializer=POCSerializer(poc,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def delete(request,POC_id):
        POC_to_delete=get_object_or_404(POC,id=POC_id)
        POC_to_delete.delete()
        return Response({'message': 'POC deleted successfully'}, status=status.HTTP_200_OK)  