import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Organisation(models.Model):
    name=models.CharField(max_length=255)
    invite_code = models.CharField(max_length=8, unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.invite_code:
            # Generate a random invite code using uuid
            self.invite_code = str(uuid.uuid4().hex)[:8].upper()
        super().save(*args, **kwargs)
    created_at = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    name=models.CharField(max_length=254)
    email=models.EmailField(max_length=254, unique=True)
    password=models.CharField(max_length=255)
    organisation=models.ForeignKey('Organisation', on_delete=models.CASCADE,null=True,blank=True)
    invite_code=models.CharField(max_length=8,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username= None
        
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
class Event(models.Model):
    name=models.CharField(max_length=255)
    date_of_event=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Email(models.Model):
    name_of_company=models.CharField(max_length=255)
    company_type=models.CharField(max_length=100)
    name_of_poc=models.CharField(max_length=100)
    position_of_poc=models.CharField(max_length=100)
    email_poc=models.EmailField()
    sponsorship_ask=models.CharField(max_length=100)
    linkedin=models.URLField()
    website=models.URLField()
    details=models.CharField(max_length=500)
    event=models.ForeignKey('Event',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    
