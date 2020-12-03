from rest_framework import serializers
from .models import Post

class PostMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'tags']

class PostReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['_id', 'title', 'body', 'tags','published_date']