from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import User
from spons_app.models import Event,Sponsorship
from users.models import User
from spons_app.serializers import EventSerializer,SponsorshipSerializer
from spons_app.permissions import IsAdmin,IsApproved

#-------------CRUD EVENT-----------------

class CreateEventView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin,IsApproved]
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        user = request.user.id
        userobj=get_object_or_404(User,id=user)
        current_organization_id = userobj.organisation
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organisation=current_organization_id)
        return Response(serializer.data)

class UpdateDeleteEventView(APIView):
    permission_classes=[IsAuthenticated,IsAdmin,IsApproved]
    authentication_classes=[JWTAuthentication]
    def patch(self,request,event_id):
        event=get_object_or_404(Event,id=event_id)
        serializer=EventSerializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,event_id):
        event_to_delete=get_object_or_404(Event,id=event_id)
        event_to_delete.delete()
        return Response({'message': 'Event deleted successfully'}, status=status.HTTP_200_OK)


#----------ADDING SPONSORS--------------

class AddSponsorView(APIView):
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
