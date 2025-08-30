from django import forms
from .models import Resource, CustomUser
from django.contrib.auth.forms import UserCreationForm


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'emotional_tone', 'tags']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'emotional_tone']
