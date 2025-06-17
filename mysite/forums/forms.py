from django import forms
from .models import Post, Thread

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 50})
        }

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'visibility']
        widgets = {
            'visibility': forms.RadioSelect
        } 