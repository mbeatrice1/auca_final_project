from django import forms
from django.contrib.auth import models
from django.db.models import fields
from django.forms import ModelForm
from .models import Congregants, Give, Profile, Project, Announcements
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Select, TextInput, Textarea


class CreateUserForm(UserCreationForm):
    class meta:
        model= User
        fields=['username','email','password1','password2']


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcements
        exclude = ['user']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user','email']


class CongForm(forms.ModelForm):
    class Meta:
        model=Congregants
        fields='__all__'
    
class GiveForm(forms.ModelForm):
    class Meta:
        model=Give
        fields='__all__'

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your name"}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your email"}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your phone"}),
            'amount': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter amount"}),            
        }
            