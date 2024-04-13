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
from spons_app.customs.permissions import IsCompanyCreator, IsPOCCreater,IsApproved
from spons_app.customs.pagination import CustomPagination


#---------------ORGANISATION DISPLAY------------

class DisplayOrganisationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def get(self,request):
        try:
            organisation_id = request.user.organisation_id
            organisation=Organisation.objects.get(id=organisation_id)
            organisation_serializer = OrganisationSerializer(organisation)
            return Response(organisation_serializer.data, status=status.HTTP_200_OK)
        except Organisation.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)
    
#---------------EVENT DISPLAY-------------------

class DisplayEventView(APIView):
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name", "start_time", "end_time"]
    search_fields = ["name"]
    ordering_fields = ["name","start_time"]
    ordering = ["start_time"]
    def get(self, request):
        organisation_id = request.query_params.get('org')
        event_id = request.query_params.get('event')
        if organisation_id is None:
            return Response({'detail': 'Organization ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        events = Event.objects.filter(organisation=organisation_id)
        if event_id:
            events = events.filter(id=event_id)
        events_serializer = EventSerializer(events, many=True)
        return Response(events_serializer.data, status=status.HTTP_200_OK)
        
#-----------CRUD COMPANY-----------------------

class CreateDisplayCompanyView(APIView):
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name", "status","updated_at","user_id"]
    search_fields = ["name","user_id","status"]
    ordering_fields = ["name","status"]
    ordering = ["name"]
    
    def get(self,request):
        organisation_id = request.query_params.get('org')
        if organisation_id is None:
            return Response({'detail': 'Organization ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        companies = Company.objects.filter(organisation=organisation_id)
        if not companies:
            return Response({'detail': 'No companies found for the given organization ID'}, status=status.HTTP_404_NOT_FOUND)
        #queryset = self.filter_queryset(companies, request)
        company_serializer = CompanySerializer(companies, many=True)
        return Response(company_serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        curr_user=request.user
        current_organization_id = curr_user.organisation 
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company=serializer.save(organisation=current_organization_id)
        companyobj=get_object_or_404(Company,id=company.id)
        companyobj.user_id= curr_user
        companyobj.save()        
        return Response(serializer.data)
    
    
class UpdateDeleteCompanyView(APIView):
    permission_classes=[IsAuthenticated,IsCompanyCreator,IsApproved]
    authentication_classes=[JWTAuthentication]
        
    @staticmethod
    def patch(request,company_id):
        company=get_object_or_404(Company,id=company_id)
        if company.user_id != request.user:
            return Response({'detail':'Permission denied'},status=status.HTTP_401_UNAUTHORIZED)
        serializer=CompanySerializer(company,data=request.data,partial=True)
    
        if serializer.is_valid():
    
            if 'status' in serializer.validated_data and serializer.validated_data['status']=='Accepted' and request.user.role not in ['admin','owner']:
                return Response({'detail':'Permission denied'},status=status.HTTP_401_UNAUTHORIZED)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def delete(request, company_id):
        company_to_delete=get_object_or_404(Company,id=company_id)
        if company_to_delete.user_id != request.user:
            return Response({'detail':'Permission denied'},status=status.HTTP_403_FORBIDDEN)
        company_to_delete.delete()
        return Response({'message': 'Company deleted successfully'}, status=status.HTTP_200_OK)

class DisplayUserCompanyView(APIView):
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name", "status","updated_at","user_id"]
    search_fields = ["name","user_id","status"]
    ordering_fields = ["name","status"]
    ordering = ["name"]
    
    def get(self, request):
        user_id = request.user.id
        companies = Company.objects.filter(user_id=user_id)
        if not companies:
            return Response({'detail': 'No companies found for the given User ID'}, status=status.HTTP_404_NOT_FOUND)
        company_serializer = CompanySerializer(companies, many=True)
        return Response(company_serializer.data, status=status.HTTP_200_OK)

class DisplayEventCompanyView(APIView):
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name", "status","updated_at","user_id"]
    search_fields = ["name","user_id","status"]
    ordering_fields = ["name","status"]
    ordering = ["name"]
    
    def get(self, request):
        event_id = request.query_params.get('event')
        if event_id is None:
            return Response({'detail': 'Event ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        pocs = POC.objects.filter(company__event=event_id)
        if not pocs:
            return Response({'detail': 'No companies found for the given event ID'}, status=status.HTTP_404_NOT_FOUND)
        poc_serializer = POCCompanySerializer(pocs, many=True)
        return Response(poc_serializer.data, status=status.HTTP_200_OK)    
#------------CRUD POC----------------

class CreateDisplayPOCView(APIView):
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
                company = get_object_or_404(Company, id=poc_data['company'])
                if company.user_id != request.user:
                    print(company.user_id, request.user)
                    return Response({'message': 'You are not allowed to add POC for this company'}, status=status.HTTP_403_FORBIDDEN)
                
                serializer.save(user=request.user.id)
                poc_objects.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        request.user.points += len(poc_objects)
        request.user.save()

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
    permission_classes=[IsAuthenticated,IsPOCCreater,IsApproved]
    authentication_classes=[JWTAuthentication]
    
    @staticmethod
    def patch(request,POC_id):
        poc=get_object_or_404(POC,id=POC_id)
        if poc.company.user_id != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        serializer=POCSerializer(poc,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def delete(request,POC_id):
        POC_to_delete=get_object_or_404(POC,id=POC_id)
        if POC_to_delete.company.user_id != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        POC_to_delete.delete()
        return Response({'message': 'POC deleted successfully'}, status=status.HTTP_200_OK)  
  
#---------------SPONSOR VIEWS-------------------
    
#sponsorship for a particular event
class DisplaySponsorsEventView(APIView):
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["money_donated","type_of_sponsorship","company.name","event"]
    search_fields = ["company.name","type_of_sponsorship"]
    ordering_fields = ["company.name","money_donated"]
    ordering = ["company.name"]
    
    def get(self, request):
        event_id = request.query_params.get('event')
        if event_id is None:
            return Response({'detail': 'Company ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        event=get_object_or_404(Event,id=event_id)
        sponsorships = event.sponsorships
        total_money_raised = event.money_raised

        sponsorship_serializer = SponsorshipSerializer(sponsorships, many=True)
        event_serializer = EventSerializer(event)

        return Response({
            "event": event_serializer.data,
            "sponsorships": sponsorship_serializer.data,
            "total_money_raised": total_money_raised
        })


