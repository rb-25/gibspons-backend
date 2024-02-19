from rest_framework import serializers
from .models import *
import uuid

#------------EVENT SERIALIZERS-------------

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['id','name','date_of_event', 'expected_reg', 'description','brochure','logo']

    
#--------------COMPANY SERIALIZERS -----------------
        
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields=['id','name','website','industry','linkedin','status']
        


#--------------POC SERIALIZERS ------------------

class POCSerializer(serializers.ModelSerializer):
    class Meta:
        model=POC
        fields=['id','name','designation','company','email','linkedin','phone']


#-----------SPONSORSHIP SERIALIZERS-------------

class SponsorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sponsorship
        fields=['id','company','event','type_of_sponsorship','money_donated','additional']

#---------AI SERIALIZER-------------------------

class AIGeneratorSerializer(serializers.Serializer):
    poc_id=serializers.IntegerField()
    event_id=serializers.IntegerField()
    additional=serializers.CharField()

#--------LEADERBOARD SERIALIZER-------------------
class LeaderboardSerializer(serializers.Serializer):
    username=serializers.CharField()
    points=serializers.IntegerField()
    