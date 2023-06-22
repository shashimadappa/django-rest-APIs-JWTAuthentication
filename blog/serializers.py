from rest_framework import serializers

from .models import BlogPost, Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email']


class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Nested serializer for author field

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'body', 'created_at', 'updated_at']
