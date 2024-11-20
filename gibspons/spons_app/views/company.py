from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from spons_app.models import Company, Sponsorship, Leaderboard
from spons_app.serializers import CompanySerializer, SponsorshipSerializer,LeaderboardSerializer

from spons_app.customs.permissions import IsCompanyCreator,IsApproved
from spons_app.customs.pagination import CustomPagination


class CompanyViewSet(ViewSet):
    """
    ViewSet to manage companies for an organization.
    """
    permission_classes = [IsAuthenticated, IsApproved]
    authentication_classes = [JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def list(self, request):
        """
        Retrieve a list of companies or a specific company for an organization.
        """
        organisation_id = request.query_params.get('org')
        company_id = request.query_params.get('id')

        if not organisation_id:
            return Response({'detail': 'Organization ID is required'}, status=HTTP_400_BAD_REQUEST)
        if request.user.organisation.id != int(organisation_id):
            return Response({'detail': 'Permission denied'}, status=HTTP_401_UNAUTHORIZED)

        companies = Company.objects.filter(organisation=organisation_id)
        if not companies:
            return Response({'detail': 'No companies found for the given organization ID'}, status=HTTP_404_NOT_FOUND)

        if company_id:
            company = get_object_or_404(Company, id=company_id)
            if company.organisation.id != int(organisation_id):
                return Response({'detail': 'Permission denied'}, status=HTTP_401_UNAUTHORIZED)
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=HTTP_200_OK)

        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request):
        """
        Create a company and its sponsorship, and update the leaderboard.
        """
        curr_user = request.user
        current_organization_id = curr_user.organisation

        name = request.data.get('name')
        website = request.data.get('website')
        existing_company = Company.objects.filter(name=name, website=website).first()

        if not existing_company:
            company_serializer = CompanySerializer(data=request.data)
            company_serializer.is_valid(raise_exception=True)
            company = company_serializer.save(organisation=current_organization_id)
        else:
            company = existing_company
            company_serializer = CompanySerializer(company)

        sponsorship_data = {
            'company': company.id,
            'event': request.data.get('event_id'),
            'contacted_by': request.user.id,
            'status': 'Not Contacted'
        }

        if Sponsorship.objects.filter(company=company.id, event=request.data.get('event_id')).exists():
            return Response({'detail': 'Company already exists for the given event'}, status=HTTP_400_BAD_REQUEST)
        
        sponsorship_serializer = SponsorshipSerializer(data=sponsorship_data)
        sponsorship_serializer.is_valid(raise_exception=True)
        sponsorship_serializer.save()

        leaderboard = Leaderboard.objects.filter(user=request.user.id, event=request.data.get('event_id')).first()
        if not leaderboard:
            leaderboard_data = {
                'event': request.data.get('event_id'),
                'user': request.user.id,
                'points': 1
            }
            leaderboard_serializer = LeaderboardSerializer(data=leaderboard_data)
            leaderboard_serializer.is_valid(raise_exception=True)
            leaderboard_serializer.save()
        else:
            leaderboard.points += 1
            leaderboard.save()

        return Response({
            'company': company_serializer.data,
            'sponsorship': sponsorship_serializer.data
        }, status=HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsCompanyCreator, IsApproved])
    def partial_update(self, request, pk=None):
        """
        Update a company partially.
        """
        company = get_object_or_404(Company, id=pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({'detail': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated, IsCompanyCreator, IsApproved])
    def destroy(self, request, pk=None):
        """
        Delete a company.
        """
        company = get_object_or_404(Company, id=pk)
        company.delete()
        return Response({'message': 'Company deleted successfully'}, status=HTTP_200_OK)