from django.db import models


    
class Company(models.Model):
    name=models.CharField(max_length=254)
    website=models.URLField()
    industry=models.CharField(max_length=50)
    status=models.CharField(max_length=20)
    user_id=models.ForeignKey('users.User', on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unique_together = ['name', 'website']
    objects = models.Manager()

class POC(models.Model):
    name=models.CharField(max_length=254)
    company=models.ForeignKey('Company',on_delete=models.CASCADE)
    email=models.EmailField()
    linkedin=models.URLField()
    phone=models.CharField(max_length=15,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Sponsorship(models.Model):
    company=models.ForeignKey('Company', on_delete=models.CASCADE)
    event=models.ForeignKey('Event',on_delete=models.CASCADE)
    type_of_sponsorship=models.CharField(max_length=254)
    money_donated=models.IntegerField()    
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
class Event(models.Model):
    name=models.CharField(max_length=255,unique=True)
    date_of_event=models.DateField()
    expected_reg=models.IntegerField(blank=True,null=True)
    brochure=models.URLField(blank=True,null=True)
    description=models.CharField(max_length=500,null=True)
    #money_raised=models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    @property
    def sponsorships(self):
        return Sponsorship.objects.filter(event=self).all()
    
    @property
    def money_raised(self):
        total=0
        for sponsorship in self.sponsorships:
            total+=sponsorship.money_donated
        return total


    