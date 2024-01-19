from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Organisation(models.Model):
    name=models.CharField(max_length=255)
    invite_code = models.CharField(max_length=8, unique=True, blank=True)
    """def save(self, *args, **kwargs):
        if not self.invite_code:
            # Generate a random invite code using uuid
            self.invite_code = str(uuid.uuid4().hex)[:8].upper()
        super().save(*args, **kwargs)"""
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