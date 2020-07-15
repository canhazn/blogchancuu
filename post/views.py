from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.models import Post, Tag, Image
from post.serializers import PostSerializer, TagSerializer, ImageSerializer
from rest_framework import permissions


class PostViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    """
    View set for list, create, update post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_fields = ["slug", "title", "tags", "images"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    """
    View set for list, create update tag
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
