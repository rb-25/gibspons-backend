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


class POCViewSet(ViewSet):
    
    """ViewSet to create, update, delete, and display POCs for a company."""

    permission_classes = [IsAuthenticated, IsApproved]
    authentication_classes = [JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name", "company", "email", "linkedin", "phone", "user"]
    search_fields = ["name", "company", "email", "linkedin", "phone", "user"]
    ordering_fields = ["name", "company", "user"]
    ordering = ["company"]

    def list(self, request):
        """Retrieve all POCs for a specific company."""
        company_id = request.query_params.get('company')
        if company_id is None:
            return Response({'detail': 'Company ID is required'}, status=HTTP_400_BAD_REQUEST)

        pocs = POC.objects.filter(company=company_id)
        if not pocs:
            return Response({'detail': 'No POC found for the given Company ID'}, status=HTTP_404_NOT_FOUND)

        serializer = POCSerializer(pocs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request):
        """Create POCs in bulk."""
        poc_data_list = request.data
        poc_objects = []

        for poc_data in poc_data_list:
            serializer = POCSerializer(data=poc_data)
            if serializer.is_valid():
                serializer.save()
                poc_objects.append(serializer.data)
            else:
                return Response({"detail": serializer.errors}, status=HTTP_400_BAD_REQUEST)

        return Response(poc_objects, status=HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='update')
    def partial_update(self, request, pk=None):
        """Update a specific POC."""
        poc = get_object_or_404(POC, id=pk)
        serializer = POCSerializer(poc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({"detail": serializer.errors}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete')
    def destroy(self, request, pk=None):
        """Delete a specific POC."""
        poc_to_delete = get_object_or_404(POC, id=pk)
        poc_to_delete.delete()
        return Response({'message': 'POC deleted successfully'}, status=HTTP_200_OK)