from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['id','name','date_of_event', 'expected_reg', 'description','brochure']

    
class DeleteEventSerializer(serializers.Serializer):
    id=serializers.IntegerField()
        
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields=['id','name','website','domain']
        

class DeleteCompanySerializer(serializers.Serializer):
    id=serializers.IntegerField()

class POCSerializer(serializers.ModelSerializer):
    class Meta:
        model=POC
        fields=['id','name','company','email','linkedin','phone']

class DeletePOCSerializer(serializers.Serializer):
    id=serializers.IntegerField()

class SponsorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sponsorship
        fields=['id','company','event','type_of_sponsorship','money_donated']
        
class DisplayMoneySerializer(serializers.Serializer):
    id=serializers.IntegerField()