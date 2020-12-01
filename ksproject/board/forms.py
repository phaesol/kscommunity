from django import forms
from .models import Post,Comment ,ReComment  
from django_summernote.widgets import SummernoteWidget     



class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
       
        fields = ('title','content','myimage')

        widgets = {                                    
            'content' : SummernoteWidget(), 
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ('body', )


class ReCommentForm(forms.ModelForm):
    class Meta:
        model = ReComment

        fields = ('body',)
