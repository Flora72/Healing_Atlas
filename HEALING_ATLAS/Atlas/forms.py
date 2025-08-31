from django import forms
from .models import Resource, CustomUser
from django.contrib.auth.forms import UserCreationForm
from .models import MoodEntry




class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'emotional_tone', 'tags']



class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            ('', 'Select your role'),
            ('survivor', 'Survivor'),
            ('ally', 'Ally'),
            ('admin', 'Admin')
        ],
        widget=forms.Select(attrs={
            'id': 'id_role',
            'class': 'form-control',
            'required': True
        })
    )

    class Meta:
        model = CustomUser  # This line is what was missing
        fields = ['username', 'email', 'password1', 'password2', 'role']

class MoodForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood', 'note']  # You’ll calculate score/sentiment later
