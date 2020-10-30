from django import forms
from .models import Post,Comment    #Comment 불러오기
from django_summernote.widgets import SummernoteWidget     



class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
       
        fields = ('title','content','myimage',)

        widgets = {                                    
            'content' : SummernoteWidget(), 
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ('body', )

# class PrivateForm(forms.ModelForm):
#     class Meta:
#         model = Private_Post
#         fields = ('title', 'content','myimage')


# class SellPostForm(forms.ModelForm):
    
#     class Meta:
#         model = Post
       
#         fields = ('category','title', 'content','myimage',)
