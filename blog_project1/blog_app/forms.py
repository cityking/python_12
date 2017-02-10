# coding: utf-8
from django import forms
from .models import Comment,Article
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content','username', 'email', 'url', 'article', 'pid']	

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
                fields = ['title','desc','content','is_recommend', 'user', 'category', 'tag'] 
