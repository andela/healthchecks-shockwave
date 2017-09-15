from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'tags', 'text')
        widgets={
        	'text': SummernoteWidget()
        }
