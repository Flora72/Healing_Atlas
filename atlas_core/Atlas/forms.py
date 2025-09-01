from django import forms
from .models import Resource, CustomUser, MoodEntry, JournalEntry
from django.contrib.auth.forms import UserCreationForm

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'emotional_tone', 'tags']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'survivor'  
        if commit:
            user.save()
        return user


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
