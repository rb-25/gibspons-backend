from django.db import models
   
class Company(models.Model):
    STATUS_CHOICES = [
        ('No Reply', 'No Reply'),
        ('In Progress', 'In Progress'),
        ('Rejected', 'Rejected'),
        ('Accepted','Accepted')
    ]
    name=models.CharField(max_length=254)
    website=models.URLField()
    industry=models.CharField(max_length=50)
    linkedin=models.URLField(null=True)
    status=models.CharField(max_length=20,default="No Reply", choices=STATUS_CHOICES)
    user_id=models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    organisation=models.ForeignKey('users.Organisation',on_delete=models.CASCADE)
    updated_at=models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unique_together = ['name', 'website']
    objects = models.Manager()

class POC(models.Model):
    name=models.CharField(max_length=254)
    company=models.ForeignKey('Company',on_delete=models.CASCADE)
    designation=models.CharField(max_length=254)
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
    additional=models.CharField(null=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
class Event(models.Model):
    organisation=models.ForeignKey('users.Organisation',on_delete=models.CASCADE)
    name=models.CharField(max_length=255,unique=True)
    date_of_event=models.DateField()
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


    