from django import forms
from .models import Resource, CustomUser
from django.contrib.auth.forms import UserCreationForm
from .models import MoodEntry
from .models import JournalEntry


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'emotional_tone', 'tags']



class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            ('', 'Select your role'),
            ('survivor', 'Survivor'),
            ('admin', 'Admin')
        ],
        widget=forms.Select(attrs={
            'id': 'id_role',
            'class': 'form-control',
            'required': True
        })
    )

    class Meta:
        model = CustomUser  
        fields = ['username', 'email', 'password1', 'password2', 'role']

class MoodForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood', 'note'] 

class JournalForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['sentiment_label', 'content']
        widgets = {
            'sentiment_label': forms.Select(attrs={
                'id': 'mood',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'id': 'entry',
                'rows': 6,
                'placeholder': "Write what’s on your heart...",
                'class': 'form-control'
            })
        }  
