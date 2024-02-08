from django.shortcuts import get_object_or_404
from django.db.models import  Sum,Count
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import User
from spons_app.models import Company
from spons_app.serializers import LeaderboardSerializer


class LeaderboardView(APIView):
    def get(self,request):
        organisation_id = request.query_params.get('org')
        leaderboard_data = User.objects.filter(organisation=organisation_id).order_by('-points')
        serializer = LeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StatusPieChartView(APIView):
    def get(self,request):
        organisation_id = request.query_params.get('org')
        data = Company.objects.filter(organisation=organisation_id).values('status').annotate(count=Count('id'))

        # Prepare data for response
        response_data = {}
        for entry in data:
            status = entry['status']
            count = entry['count']

            response_data[status] = count

        return Response(response_data)
        