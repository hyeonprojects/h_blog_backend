from rest_framework import serializers
from .models import Post

class PostMakeSerializer(serializers.ModelSerializer):
    tags = serializers.JSONField(allow_null=True)
    class Meta:
        model = Post
        fields = ['title', 'body', 'tags']

class PostReadSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(max_length=100)
    tags = serializers.JSONField(allow_null=True)
    class Meta:
        model = Post
        fields = ['_id', 'title', 'body', 'tags', 'published_date']