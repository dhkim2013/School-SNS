from django import forms
from .models import Class, Post, Comment

class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name', 'code')

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
