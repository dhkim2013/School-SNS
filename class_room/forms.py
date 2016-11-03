from django import forms
from .models import Class, Post

class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name', 'code')

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')
