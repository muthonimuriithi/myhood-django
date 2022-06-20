from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    bio = forms.CharField() 

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['avatar','status']
        
class NeighbourHoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        exclude = ('admin',)

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('user', 'neighbourhood')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'neighbourhood')        