from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.models import Post, Tag, Image
from post.serializers import PostSerializer, TagSerializer, ImageSerializer


class PostViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    """
    View set for list, create, update post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_fields = ["slug", "title", "tags", "images"]


class TagViewSet(viewsets.ModelViewSet):
    """
    View set for list, create update tag
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
