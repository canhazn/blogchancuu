from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from post.serializers import TagSerializer
from django.urls import reverse

TAG_URL = reverse('post:tag-list')

class TestTagApi(TestCase):
    """
    Test tag api
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_empty_tag(self):
        """
        Test creating empty tag is failue
        """
        tag = {}
        
        res = self.client.post(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)        

    def test_list_tag(self):
        """
        Test list tag returns data
        """
        tag = Tag.objects.create(
            title="Test tag",
            slug ="test-tag"
        )

        res = self.client.get(TAG_URL)
        serializer = TagSerializer(Tag.objects.all(), many=True)        
        self.assertEqual(res.data, serializer.data)