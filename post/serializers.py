from rest_framework import serializers
from core.models import Post, Tag, Image


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        # exclude = ["id"]


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'images', 'tags', 'title',
                  'slug', 'content', 'created_on']        
        depth = 1
