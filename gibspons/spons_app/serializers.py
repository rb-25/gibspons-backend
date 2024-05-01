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
    
    class Meta:
        model=Company
        fields=['id','name','website','industry','linkedin']


#--------------POC SERIALIZERS ------------------

class POCSerializer(serializers.ModelSerializer):
    
    company_name = serializers.CharField(source='company.name',required=False,read_only=True)    
    class Meta:
        model=POC
        fields=['id','company','name','email','linkedin','phone','company_name']
        
    def create(self, validated_data):
        validated_data.pop('user', None)
        company = validated_data.pop('company')  
        poc = POC.objects.create(company=company, **validated_data)  
        return poc


class POCCompanySerializer(serializers.ModelSerializer):
    
    updated_at = serializers.DateField(source='sponsor.updated_at',required=False,read_only=True)
    company_name = serializers.CharField(source='company.name',required=False,read_only=True)  
    name = serializers.CharField()
    added_by = serializers.CharField(source='sponsor.contacted_by.username',required=False,read_only=True)
    status = serializers.CharField(source='sponsor.status',required=False,read_only=True)  

    class Meta:
        model = POC
        fields = ['updated_at','company_name', 'name', 'added_by', 'status']
        
#-----------SPONSORSHIP SERIALIZERS-------------

class SponsorshipSerializer(serializers.ModelSerializer):
    
    company_name = serializers.CharField(source='company.name',required=False,read_only=True)
    poc_name=serializers.CharField(source='poc.name',required=False,read_only=True)
    user_name = serializers.CharField(source='contacted_by.username',required=False,read_only=True)
    event_name = serializers.CharField(source='event.name',required=False,read_only=True)
    
    class Meta:
        model=Sponsorship
        fields=['id','company','company_name','poc','poc_name','event','event_name','contacted_by','user_name','updated_at','status','remarks','type_of_sponsorship','money_donated','additional']

#---------AI SERIALIZER-------------------------

class AIGeneratorSerializer(serializers.Serializer):
    
    poc_id=serializers.IntegerField()
    event_id=serializers.IntegerField()
    additional=serializers.CharField(required=False,allow_blank=True)

#--------LEADERBOARD SERIALIZER-------------------

class LeaderboardSerializer(serializers.ModelSerializer):
    
    user_name = serializers.CharField(source='user.username',required=False,read_only=True)
    event_name = serializers.CharField(source='event.name',required=False,read_only=True)
    
    class Meta:
        model=Leaderboard
        fields=['user','event','points','user_name','event_name']
    