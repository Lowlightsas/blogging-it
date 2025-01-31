from django import forms
from .models import Post,PostAttachment,Comment

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title','category','body','status']

class PostAttachmentForm(forms.ModelForm):

    class Meta:
        model = PostAttachment
        fields = ['photo','caption']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        
class SearchForm(forms.Form):
    query = forms.CharField()