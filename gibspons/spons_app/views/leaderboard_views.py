from django.db.models import  Count
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import User
from spons_app.models import Company,Sponsorship,Leaderboard
from spons_app.serializers import LeaderboardSerializer


class LeaderboardView(APIView):
    
    """ View to display leaderboard by event """
    
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        event_id = request.query_params.get('event')
        leaderboard_data = Leaderboard.objects.filter(event=event_id).order_by('-points')
        serializer = LeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StatusPieChartView(APIView):
    
    """ View to display pie chart of all status by event """
    
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        event = request.query_params.get('event')
        data = Sponsorship.objects.filter(event_id=event).values('status').annotate(count=Count('id'))

        # Prepare data for response
        response_data = {}
        for entry in data:
            status = entry['status']
            count = entry['count']

            response_data[status] = count

        return Response(response_data)
        