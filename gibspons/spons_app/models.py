from django.db import models

class Company(models.Model):
    
    """ Model for Company details """
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        unique_together = ['name', 'website','organisation']
    
    name=models.CharField(max_length=254)
    website=models.URLField()
    industry=models.CharField(max_length=50)
    linkedin=models.URLField(null=True)    
    organisation=models.ForeignKey('users.Organisation',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class POC(models.Model):
    
    """ Model for Point of Contact details"""
    
    class meta:
        verbose_name = 'POC'
        verbose_name_plural = 'POCs'
        
    name=models.CharField(max_length=254)
    company=models.ForeignKey('Company',on_delete=models.CASCADE)
    designation=models.CharField(max_length=254)
    email=models.EmailField()
    linkedin=models.URLField()
    phone=models.CharField(max_length=15,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Sponsorship(models.Model):
    
    """ Model for Sponsor details for an event """
    
    STATUS_CHOICES = [
        ('Not Contacted', 'Not Contacted'),
        ('No Reply', 'No Reply'),
        ('In Progress', 'In Progress'),
        ('Rejected', 'Rejected'),
        ('Accepted','Accepted')
    ]
        
    company=models.ForeignKey('Company', on_delete=models.CASCADE)
    poc=models.ForeignKey('POC',on_delete=models.CASCADE,null=True)
    event=models.ForeignKey('Event',on_delete=models.CASCADE)
    contacted_by=models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    status=models.CharField(max_length=20,default="Not Contacted", choices=STATUS_CHOICES)
    type_of_sponsorship=models.CharField(max_length=254,blank=True,null=True)
    money_donated=models.IntegerField(blank=True,null=True,default=0)
    additional=models.CharField(null=True)
    updated_at=models.DateField(auto_now=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
class Event(models.Model):
    """ Model for Event details """
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        
    organisation=models.ForeignKey('users.Organisation',on_delete=models.CASCADE)
    name=models.CharField(max_length=255,unique=True)
    start_date=models.DateField()
    end_date=models.DateField()
    expected_reg=models.IntegerField(blank=True,null=True)
    brochure=models.URLField(blank=True,null=True)
    description=models.CharField(max_length=500,null=True)
    logo=models.URLField(null=True, max_length=None)
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


    