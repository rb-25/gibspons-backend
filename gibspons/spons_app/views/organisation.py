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


class DisplayOrganisationView(APIView):
    
    """ View to display an organisation """
    
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