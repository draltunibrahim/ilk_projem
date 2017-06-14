from django import forms
from post.models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image'
        ]

class CommentFrom(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'name',
            'content'
        ]