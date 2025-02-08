from django import forms
from .models import Post,PostAttachment,Comment,ContactMessage

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

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','category','body','status']
    
class PostAttachmentEditForm(forms.ModelForm):
    class Meta:
        model = PostAttachment
        fields = ['photo','caption']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message'}),
        }
