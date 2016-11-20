from django import forms
from .models import CustumUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):

    class Meta:
        model = CustumUser
        fields = ("username", "name", "password1", "password2", "job",)

class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustumUser
        fields = ('profileImage',)
