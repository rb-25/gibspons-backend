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
        fields=['id','name','website','industry','linkedin','status','event']
        


#--------------POC SERIALIZERS ------------------

class POCSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name',required=False)
    class Meta:
        model=POC
        fields=['id','name','designation','company','company_name','email','linkedin','phone']


class POCCompanySerializer(serializers.ModelSerializer):
    updated_at = serializers.DateField(source='company.updated_at')
    company_name = serializers.CharField(source='company.name')  
    name = serializers.CharField()
    added_by = serializers.CharField(source='company.user_id.username')
    status = serializers.CharField(source='company.status')  

    class Meta:
        model = POC
        fields = ['updated_at','company_name', 'name', 'added_by', 'status']
#-----------SPONSORSHIP SERIALIZERS-------------

class SponsorshipSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name')
    class Meta:
        model=Sponsorship
        fields=['id','company','company_name','event','type_of_sponsorship','money_donated','additional']

#---------AI SERIALIZER-------------------------

class AIGeneratorSerializer(serializers.Serializer):
    poc_id=serializers.IntegerField()
    event_id=serializers.IntegerField()
    additional=serializers.CharField()

#--------LEADERBOARD SERIALIZER-------------------
class LeaderboardSerializer(serializers.Serializer):
    username=serializers.CharField()
    points=serializers.IntegerField()
    