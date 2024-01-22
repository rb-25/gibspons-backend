from django.shortcuts import get_object_or_404
from django.db.models import  Sum,Count
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import *
from ..permissions import *

#-----------CRUD COMPANY-----------------------

class CreateCompanyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company=serializer.save()
        companyobj=get_object_or_404(Company,id=company.id)
        companyobj.user_id= request.user
        companyobj.save()        
        return Response(serializer.data)
    
class UpdateCompanyView(APIView):
    permission_classes=[IsAuthenticated,IsCompanyCreator]
    authentication_classes=[JWTAuthentication]
    def patch(self,request,company_id):
        company=get_object_or_404(Company,id=company_id)
        if company.user_id != request.user:
            return Response({'detail':'Permission denied'},status=status.HTTP_403_FORBIDDEN)
        serializer=CompanySerializer(company,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class DeleteCompanyView(APIView):
    permission_classes=[IsAuthenticated,IsCompanyCreator]
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        serializer=DeleteCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_to_delete=get_object_or_404(Company,id=serializer.data['id'])
        if company_to_delete.user_id != request.user:
            return Response({'detail':'Permission denied'},status=status.HTTP_403_FORBIDDEN)
        company_to_delete.delete()
        return Response({'message': 'Company deleted successfully'}, status=status.HTTP_200_OK)
    
#------------CRUD POC----------------

class CreatePOCView(APIView):
    permission_classes = [IsAuthenticated]
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
        pocobj.user= request.user
        pocobj.save()
        return Response(serializer.data)

class UpdatePOCView(APIView):
    permission_classes=[IsAuthenticated,IsPOCCreater]
    authentication_classes=[JWTAuthentication]
    def patch(self,request,POC_id):
        poc=get_object_or_404(POC,id=POC_id)
        if poc.company.user_id != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        serializer=POCSerializer(poc,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class DeletePOCView(APIView):
    permission_classes=[IsAuthenticated,IsPOCCreater]
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        serializer=DeletePOCSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        POC_to_delete=get_object_or_404(POC,id=serializer.data['id'])
        if POC_to_delete.company.user_id != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        POC_to_delete.delete()
        return Response({'message': 'POC deleted successfully'}, status=status.HTTP_200_OK)
    

class DisplayMoney(APIView):
    def post(self, request):
        serializer=DisplayMoneySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event=get_object_or_404(Event,id=serializer.data['id'])
        sponsorships = event.sponsorships
        total_money_raised = event.money_raised

        sponsorship_serializer = SponsorshipSerializer(sponsorships, many=True)
        event_serializer = EventSerializer(event)

        return Response({
            "event": event_serializer.data,
            "sponsorships": sponsorship_serializer.data,
            "total_money_raised": total_money_raised
        })
        
"""class LeaderboardView(APIView):
    #permission_classes=[]
    def get_queryset(self):
        queryset = Company.objects.values('user').annotate(company_count=Count('user')).order_by('-company_count')
        return queryset"""
    