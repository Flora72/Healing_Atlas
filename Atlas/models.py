from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# 🌿 Custom User Model
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

    def __str__(self):
        return self.username

# 🧶 Survivor Profile
class SurvivorProfile(models.Model):
    name = models.CharField(max_length=100)
    story = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 🪷 Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# 📚 Resource Model
class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')
    emotional_tone = models.CharField(max_length=20, choices=[
        ('soft', '🌸 Soft'),
        ('neutral', '🌿 Neutral'),
        ('alert', '⚠️ Alert'),
    ])
    tags = models.ManyToManyField(Tag, blank=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
