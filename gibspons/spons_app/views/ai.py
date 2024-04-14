from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import markdown
from users.models import Organisation,User
from spons_app.serializers import AIGeneratorSerializer
from spons_app.models import Company,POC,Event
from spons_app.config import model

class EmailGeneratorView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        serializer=AIGeneratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        poc=get_object_or_404(POC,id=serializer.validated_data['poc_id'])
        company=get_object_or_404(Company,id=poc.company.id)
        organisation=get_object_or_404(Organisation,id=company.organisation.id)
        event=get_object_or_404(Event, id=serializer.validated_data['event_id'])
        user=get_object_or_404(User,id=request.user.id)
        prompt = f"Ignore all previous prompts. Here is the information you are provided with. {organisation.name} is an organisation from {organisation.location} and they are organising an event {event.name}. The event is being hosted on {event.date_of_event} with expected registrations {event.expected_reg}. Additional information about the event is {event.description}. Assume you are {user.name}, a manager at {organisation.name} Write me a professional email inviting the POC {poc.name} from {company.name} with the designation {poc.designation} to sponsor the event hosted by our organisation. The company is in the {company.industry} industry. Our organisation is in the {organisation.industry}. Mention how the company’s goals align with our interests and the goals we aim to achieve through our event as well. Make sure it sounds professional and do not use any informal words. It should also sound convincing. Begin the email with a short description (1-2 lines) of who you are and the organisation you work at. The next paragraph should describe the event. The next paragraph should ask for a sponsorship from the company. Mention that both monetary and inkind sponsorships would be acceptable. Lastly ask them to visit the organisation website and refer to the brochure attatched in the email. Additional information given is {serializer.validated_data['additional']} Write this email in 200 to 300 words. "
        response = model.generate_content(prompt)
        response_html=markdown.markdown(response.text).replace('\n','')
        return Response({"message":response_html})
        
class LinkedInGeneratorView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        serializer=AIGeneratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        poc=get_object_or_404(POC,id=serializer.validated_data['poc_id'])
        company=get_object_or_404(Company,id=poc.company.id)
        organisation=get_object_or_404(Organisation,id=company.organisation.id)
        event=get_object_or_404(Event, id=serializer.validated_data['event_id'])
        user=get_object_or_404(User,id=request.user.id)
        prompt = f"Ignore all previous prompts. Here is the information you are provided with. {organisation.name} is an organisation from {organisation.location} and they are organising an event {event.name}. The event is being hosted on {event.date_of_event} with expected registrations {event.expected_reg}. Additional information about the event is {event.description}. Assume you are {user.name}, a manager at {organisation.name} Write me a professional linkedin request inviting the POC {poc.name} from {company.name} with the designation {poc.designation} to sponsor the event hosted by our organisation. The company is in the {company.industry} industry. Our organisation is in the {organisation.industry}. Additional information given is {serializer.validated_data['additional']} Write this linkedin in 50 to 100 words. "
        response = model.generate_content(prompt)
        response_html=markdown.markdown(response.text).replace('\n','')
        return Response({"message":response_html})
        