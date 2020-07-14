from django.test import TestCase
from core import models


class ModelTest(TestCase):
    """Test models initialization"""
    def test_post_str(self):
        """Test post represents slug"""
        post = models.Post.objects.create(
            title="Test post",
            slug="test-post",
            content="This is test post content"
        )        
        self.assertEqual(post.slug, str(post))

    def test_tag_str(self):
        """Test tag represent slug"""
        tag = models.Tag.objects.create(
            title="Test tag",
            slug ="test-tag"
        )

        self.assertEqual(tag.slug, str(tag))