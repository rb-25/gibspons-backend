from rest_framework import serializers
from .models import User,Organisation
import uuid

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','password']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    
    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance= self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organisation
        fields=['id','name','invite_code']
        extra_kwargs = {
            'name': {'required': False},
            'invite_code': {'validators': []},  # Disable default uniqueness validator
        }
    
    def create(self,validated_data):
        invite_code=str(uuid.uuid4())
        truncated_ic=invite_code[:8]
        validated_data['invite_code']=truncated_ic
        instance=self.Meta.model(**validated_data)
        instance.save()
        return instance

class JoinOrganisationSerializer(serializers.Serializer):
    invite_code = serializers.CharField()

class ChangeRoleSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.CharField()

class DeleteUserSerializer(serializers.Serializer):
    email = serializers.EmailField()