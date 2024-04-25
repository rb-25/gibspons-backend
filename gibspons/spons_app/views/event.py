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


class CreateEventView(APIView):
    
    """ View to create an event for an organization. Only admins can create events.""" 
    
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
    
    """View to update and delete an event. Only admins can update and delete events."""
    
    permission_classes=[IsAuthenticated,IsAdmin,IsApproved]
    authentication_classes=[JWTAuthentication]
    def patch(self,request,event_id):
        event=get_object_or_404(Event,id=event_id)
        serializer=EventSerializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"detail" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,event_id):
        event_to_delete=get_object_or_404(Event,id=event_id)
        event_to_delete.delete()
        return Response({'message': 'Event deleted successfully'}, status=status.HTTP_200_OK)

class DisplayEventView(APIView):
    
    """View to display events for an organization."""
    
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