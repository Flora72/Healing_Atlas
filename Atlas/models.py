from django.db import models

class SurvivorProfile(models.Model):
    name = models.CharField(max_length=100)
    story = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
