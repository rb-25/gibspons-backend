from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
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

class EventViewSet(ModelViewSet):
        
        """Viewset to perform CRUD operations on events."""
        
        queryset = Event.objects.all()
        serializer_class = EventSerializer
        permission_classes = [IsAuthenticated,IsApproved]
        authentication_classes=[JWTAuthentication]
        pagination_class = CustomPagination
        filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
        filterset_fields = ["id","name", "start_date", "end_date"]
        search_fields = ["id","name","start_date"]
        ordering_fields = ["start_date","name"]
        ordering = ["-start_date"]
        
        def get_queryset(self):
            user = self.request.user.id
            userobj=get_object_or_404(User,id=user)
            current_organization_id = userobj.organisation
            return Event.objects.filter(organisation=current_organization_id)
        
        def get_permissions(self):
            permission_classes = [IsAuthenticated]
            if self.action in ["create","update","partial_update","destroy"]:
                permission_classes.append(IsAdmin)

            return [permission() for permission in permission_classes]
        
        def create(self, request):
            user = request.user.id
            userobj=get_object_or_404(User,id=user)
            current_organization_id = userobj.organisation
            serializer = EventSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(organisation=current_organization_id)
            return Response(serializer.data)
        
        def partial_update(self, request, pk=None):
            event = get_object_or_404(Event,id=pk,organisation=request.user.organisation)
            serializer = EventSerializer(event, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)