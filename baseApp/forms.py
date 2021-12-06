from django.db.models import fields
from django.forms import ModelForm
from . models import *
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'



class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user', 'likes', 'dislikes']
        
        widgets = {
          'post': forms.TextInput(attrs={'rows':50, 'cols':100}),
        }