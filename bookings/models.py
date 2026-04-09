from django.db import models
from django.conf import settings
from auth_app.models import TourGuide

# Create your models here.
class TourLocation(models.Model):
    location=models.CharField(max_length=100,null=True,blank=True)
    hotel=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return f"{self.location} - {self.hotel}"


class PackageHighlights(models.Model):
    highlight=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.highlight

class Transport(models.Model):
    vehicle=models.CharField(max_length=100,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.vehicle


class Packages(models.Model):
    tour_guide = models.ForeignKey('auth_app.TourGuide', on_delete=models.CASCADE, related_name='packages',null= True,blank=True)
    title=models.CharField(max_length=100,null=True,blank=True)
    main_location=models.CharField(max_length=100,null=True,blank=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to='packageImage/')
    location=models.ManyToManyField(TourLocation, related_name='tourlocation')
    highlight=models.ManyToManyField(PackageHighlights,related_name='packagehighlights')
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    details=models.TextField()
    complementary=models.CharField(max_length=20,null=True,blank=True ,choices=[('breakfast', 'Breakfast'), ('all_meals', 'All Meals'),('breakfast_lunch','Breakfast & Lunch')])
    transport=models.ManyToManyField(Transport,related_name='transport')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

    
