from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Organisation(models.Model):
    name=models.CharField(max_length=255)
    invite_code = models.CharField(max_length=8, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('owner', 'Owner'),
        ('admin', 'Admin'),
    ]
    name=models.CharField(max_length=254)
    email=models.EmailField(max_length=254, unique=True)
    password=models.CharField(max_length=255)
    organisation=models.ForeignKey('Organisation', on_delete=models.CASCADE,null=True,blank=True)
    role=models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    username= None
        
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects = models.Manager()
    

    