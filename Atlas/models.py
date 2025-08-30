from django.db import models

class SurvivorProfile(models.Model):
    name = models.CharField(max_length=100)
    story = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=[
        ('survivor', 'Survivor'),
        ('ally', 'Ally'),
        ('admin', 'Admin'),
    ])
    emotional_tone = models.CharField(max_length=20, choices=[
        ('soft', 'Soft'),
        ('neutral', 'Neutral'),
        ('alert', 'Alert'),
    ])
    safety_flag = models.BooleanField(default=False)
