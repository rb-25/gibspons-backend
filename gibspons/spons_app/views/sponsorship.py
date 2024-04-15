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
   

class UpdateSponsorView(APIView):
    
    """ View to update """
    
    permission_classes=[IsAuthenticated,IsCompanyCreator,IsApproved]
    authentication_classes=[JWTAuthentication]
        
    @staticmethod
    def patch(request,sponsor_id):
        sponsor=get_object_or_404(Sponsorship,id=sponsor_id)
        serializer=SponsorshipSerializer(sponsor,data=request.data,partial=True)    
        if serializer.is_valid():
            if any(serializer.validated_data.get(key) for key in ['money_donated', 'additional', 'type_of_sponsorship']) and request.user.role not in ['admin', 'owner']:
                return Response({'detail': 'Permission denied'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if 'status' in serializer.validated_data and serializer.validated_data['status']=='Accepted' and request.user.role not in ['admin','owner']:
                return Response({'detail':'Permission denied'},status=status.HTTP_401_UNAUTHORIZED)
            
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DisplaySponsorsEventView(APIView):
    
    """View to display sponsors for a particular organisation and event"""
    
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["money_donated","type_of_sponsorship","company.name","event"]
    search_fields = ["company.name","type_of_sponsorship"]
    ordering_fields = ["company.name","money_donated"]
    ordering = ["company.name"]
    
    def get(self, request):
        org_id = request.user.organisation.id
        event_id = request.query_params.get('event')
        if event_id is not None:
            event=get_object_or_404(Event,id=event_id)
            sponsorships = event.sponsorships
            if sponsorships.count() == 0:
                return Response({'detail': 'No sponsors found for the given Event ID'}, status=status.HTTP_404_NOT_FOUND)
            
            total_money_raised = event.money_raised

            sponsorship_serializer = SponsorshipSerializer(sponsorships, many=True)
            event_serializer = EventSerializer(event)

            return Response({
            "event": event_serializer.data,
            "sponsorships": sponsorship_serializer.data,
            "total_money_raised": total_money_raised
            })
        else:
            sponsor= Sponsorship.objects.filter(company__organisation=org_id)
            if not sponsor:
                return Response({'detail': 'No sponsors found for the given Organisation ID'}, status=status.HTTP_404_NOT_FOUND)    
            sponsor_serializer = SponsorshipSerializer(sponsor, many=True)
            return Response(sponsor_serializer.data, status=status.HTTP_200_OK)
        
class DisplayUserCompanyView(APIView):
    
    """View to display companies for a particular user"""
    
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name", "status","updated_at","contacted_by"]
    search_fields = ["name","contacted_by","status"]
    ordering_fields = ["name","status"]
    ordering = ["name"]
    
    def get(self, request):
        user_id = request.user.id
        sponsors = Sponsorship.objects.filter(contacted_by=user_id)
        if not sponsors:
            return Response({'detail': 'No companies found for the given User ID'}, status=status.HTTP_404_NOT_FOUND)
        sponsor_serializer = SponsorshipSerializer(sponsors, many=True)
        return Response(sponsor_serializer.data, status=status.HTTP_200_OK)


class AddAcceptedView(APIView):
    
    """View to add accepted sponsorships (status=Accepted) to the event"""
    
    permission_classes=[IsAuthenticated,IsAdmin,IsApproved]
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        serializer=SponsorshipSerializer(data=request.data)
        if serializer.is_valid():           
            existing_sponsorship=Sponsorship.objects.filter(company=serializer.validated_data['company']).first()
            if existing_sponsorship and 'money_donated' in serializer.validated_data :
                existing_sponsorship.money_donated+=serializer.validated_data['money_donated']
                existing_sponsorship.save()
            elif existing_sponsorship and 'additional' in serializer.validated_data:
                existing_sponsorship.additional=serializer.validated_data['additional']
                existing_sponsorship.save()
            else:
                serializer.save()                
        event = get_object_or_404(Event,id=serializer.data['event'])
        sponsorships = event.sponsorships
        money_raised = event.money_raised
        for sponsorship in sponsorships:
            company_name = sponsorship.company.name
            print(f"Sponsorship by {company_name}: {sponsorship.money_donated}")
        print(f"Money Raised: {money_raised}")
        return Response(serializer.data,status=status.HTTP_200_OK)