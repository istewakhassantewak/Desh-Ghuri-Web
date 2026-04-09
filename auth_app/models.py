from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import CustomUserManager
from django.apps import apps

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=[('traveler', 'Traveler'), ('tour_guide', 'Tour Guide')])
    address = models.CharField(max_length=255, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Traveler(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='traveler_profile')
    preferences = models.TextField(blank=True, null=True)
    interests = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Traveler: {self.user.email}"


class TourGuide(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='guide_profile')
    location = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    expertise = models.CharField(max_length=255, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Tour Guide: {self.user.email}"

