from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

class Organisation(models.Model):
    name=models.CharField(max_length=255)
    invite_code = models.CharField(max_length=8, unique=True, blank=True)
    industry=models.CharField(max_length=255)
    location=models.CharField(max_length=254,null=True,blank=True)
    logo=models.URLField()    #how do i validate that its an image
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('owner', 'Owner'),
        ('admin', 'Admin'),
    ]
    is_approved=models.BooleanField(default=False)
    name=models.CharField(max_length=254)
    username= models.CharField(max_length=254, unique=True)
    email=models.EmailField(max_length=254, unique=True)    
    password=models.CharField(max_length=255)
    organisation=models.ForeignKey('Organisation', on_delete=models.CASCADE,null=True,blank=True)
    role=models.CharField(max_length=20, null=True, choices=ROLE_CHOICES)
    points=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    REQUIRED_FIELDS=[]
    
    

    