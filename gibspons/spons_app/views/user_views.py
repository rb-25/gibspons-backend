from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import User
from spons_app.models import Event,Company, POC
from spons_app.serializers import POCSerializer, CompanySerializer, EventSerializer, SponsorshipSerializer
from spons_app.permissions import IsCompanyCreator, IsPOCCreater,IsApproved

#---------------EVENT DISPLAY-------------------

class DisplayEventView(APIView):
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]

    def get(request):
        organisation_id = request.query_params.get('org')
        if organisation_id is None:
            return Response({'detail': 'Organization ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        events=Event.objects.filter(organisation=organisation_id)
        events_serializer = EventSerializer(events, many=True)
        return Response(events_serializer.data, status=status.HTTP_200_OK)
    
#-----------CRUD COMPANY-----------------------

class CreateDisplayCompanyView(APIView):
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    
    @staticmethod
    def get(request):
        organisation_id = request.query_params.get('org')
        if organisation_id is None:
            return Response({'detail': 'Organization ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        companies = Company.objects.filter(organisation=organisation_id)
        if not companies:
            return Response({'detail': 'No companies found for the given organization ID'}, status=status.HTTP_404_NOT_FOUND)
        company_serializer = CompanySerializer(companies, many=True)
        return Response(company_serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def post(request):
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


    
#------------CRUD POC----------------

class CreateDisplayPOCView(APIView):
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    
    def post(self,request):
        serializer = POCSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        curr_user=request.user             
        company=get_object_or_404(Company,id=serializer.validated_data['company'].id)
        if company.user_id != curr_user:
            return Response({'message':'You are not allowed to add POC for this company'},status=status.HTTP_403_FORBIDDEN)        
        poc=serializer.save()
        pocobj=get_object_or_404(POC,id=poc.id)
        pocobj.user= request.user.id
        pocobj.save()
        userobj=get_object_or_404(User,id=request.user.id)
        userobj.points+=1
        userobj.save()
        return Response(serializer.data)
    
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


