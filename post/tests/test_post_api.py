from django.test import TestCase
from core.models import Post, Tag
from post.serializers import PostSerializer
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from django.utils.text import slugify

POST_URL = reverse('post:post-list')


class TestPostApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_post(self):
        """
        Test listing posts
        """
        res = self.client.get(POST_URL)
        posts = Post.objects.all()
        serializer = PostSerializer(many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_emty_post(self):
        """
        Test creating empty post successfull
        """
        post = {}
        res = self.client.post(POST_URL, post)
    
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['slug'], slugify(timezone.now()))
        
