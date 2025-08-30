from django import forms
from .models import Resource, CustomUser
from django.contrib.auth.forms import UserCreationForm


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'emotional_tone', 'tags']

class CustomUserCreationForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=[('', 'Select your role'), ('survivor', 'Survivor'), ('ally', 'Ally'), ('admin', 'Admin')],
        widget=forms.Select(attrs={
            'id': 'id_role',
            'class': 'form-control',
            'required': True
        })
    )
