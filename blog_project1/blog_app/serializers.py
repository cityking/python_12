from rest_framework import serializers
from .models import Article 

class ArticleSerializer(serializers.ModelSerializer):
        class Meta:
                model = Article 
                fields = ['title','desc','content','is_recommend', 'user', 'category', 'tag'] 
