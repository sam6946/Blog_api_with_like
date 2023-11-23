from datetime import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blogs, Likes


class AboutUserSerializer(serializers.ModelSerializer):
    blogs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'blogs']
    
    def get_blogs(self, obj):
        return Blogs.objects.filter(posted_by_id=obj.id).values_list('title', flat=True)



class GetBlogsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='posted_by.username')
    author_id = serializers.ReadOnlyField(source='posted_by.id')
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Blogs
        fields = ['id', 'title', 'created_at', 'author', 'author_id', 'content', 'likes']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.last_updated_at = datetime.now()
        instance.save()
        return instance

    def get_likes(self, blog):
        return Likes.objects.filter(blog=blog).count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ["id"]