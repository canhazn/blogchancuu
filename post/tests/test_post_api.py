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
        self.assertIsNotNone(res.data['slug'])
        self.assertIsNotNone(res.data['created_on'])

    def test_create_post_with_tag(self):
        """
        Test creating post with assosiated tag
        """

        tag1 = Tag.objects.create(
            title="Test tag",
            slug="test-tag"
        )

        tag2 = Tag.objects.create(
            title="Test tag 2",
            slug="test-tag-2"
        )

        payload = {
            'title': "Test post",
            "slug": "test-post",
            "content": "empyt contemt",
            "tags": [tag1.id, tag2.id]
        }

        res = self.client.post(POST_URL, payload)
        print(res.data)
        post = Post.objects.get(id=res.data['id'])
        tags = post.tags.all()
        print(tags)
