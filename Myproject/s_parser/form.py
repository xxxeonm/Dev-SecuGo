from django import forms

from .models import BlogData

class PostForm(forms.ModelForm):

    class Meta:
        model = BlogData
        fields = ('title', 'link',)