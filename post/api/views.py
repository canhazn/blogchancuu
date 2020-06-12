from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from  rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.

from ..models import Post, Tag, Image
from .serializer import PostSerializer, TagSerializer, ImageSerializer
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

class TagDetail(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'

class ImageList(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

@api_view(['GET'])
def apiOverView(request):
    api_urls = {
        'List' : 'post-list',
        'Detail': 'post-detail'
    }
    return Response(api_urls)

class PostList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    pagination_class = PostLimitOffsetPagination

@api_view(['GET'])
def postList(request):
    queryset = Post.objects.all()
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data)

class PostDetail(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


@api_view(['GET'])
def postDetail(request, slug):
    return Response({})