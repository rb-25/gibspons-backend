from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from spons_app.models import Event

class Organisation(models.Model):
    name=models.CharField(max_length=255)
    invite_code = models.CharField(max_length=8, unique=True, blank=True)
    industry=models.CharField(max_length=255)
    location=models.CharField(max_length=254,null=True,blank=True)
    logo=models.URLField()    #how do i validate that its an image
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    @property
    def events(self):
        return Event.objects.filter(organisation=self).all()
    
    @property
    def total_money_raised(self):
        total=0
        for event in self.events:
            print(event.money_raised)
            total+=event.money_raised
        return total
    
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
    profile_pic=models.URLField(null=True)
    organisation=models.ForeignKey('Organisation', on_delete=models.CASCADE,null=True,blank=True)
    role=models.CharField(max_length=20, null=True, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    REQUIRED_FIELDS=[]
    
    

    