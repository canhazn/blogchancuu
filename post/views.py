from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.models import Post, Tag
from post.serializers import PostSerializer, TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    View set for list, create, update post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    View set for list, create update tag
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer