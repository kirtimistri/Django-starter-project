from django .forms import ModelForm
from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
    
class ProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        exclude=['user']
        widgets={
            'profile_picture': forms.FileInput(),
            'display_name':forms.TextInput(attrs={'placeholder':'Add display name'}),
            'info':forms.Textarea(attrs={'rows':3,'placeholder':'Add display name'})
        }

class EmailForm(ModelForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=['email']