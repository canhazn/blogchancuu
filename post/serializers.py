from rest_framework import serializers
from core.models import Post, Tag, Image


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ["id"]


class ImageSerializer(serializers.ModelSerializer):
    # post = serializers.

    # url = serializers.SerializerMethodField
    class Meta:
        model = Image
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ['images', 'id', 'tags', 'title',
                  'slug', 'content', 'created_on']
        read_only_fields = ["id"]
        depth = 1
