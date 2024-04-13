from rest_framework import serializers
from .models import *
import uuid

#------------EVENT SERIALIZERS-------------

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['id','name','start_date','end_date', 'expected_reg', 'description','brochure','logo','money_raised']

    
#--------------COMPANY SERIALIZERS -----------------
        
class CompanySerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.name',required=False,read_only=True)
    user_name = serializers.CharField(source='user.name',required=False,read_only=True) 
    class Meta:
        model=Company
        fields=['id','name','website','industry','linkedin','status','event','event_name','user_id','user_name']
        


#--------------POC SERIALIZERS ------------------

class POCSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name',required=False,read_only=True)
    class Meta:
        model=POC
        fields=['id','name','designation','company','company_name','email','linkedin','phone','event']
    def create(self, validated_data):
        validated_data.pop('user', None)
        company = validated_data.pop('company')  
        poc = POC.objects.create(company=company, **validated_data)  
        return poc


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
    