from django.test import TestCase
from core import models

import tempfile
import os

from PIL import Image

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
            slug="test-tag"
        )

        self.assertEqual(tag.slug, str(tag))

    def test_image_str(self):
        """Test image represent slug"""

        post = models.Post.objects.create(
            title="Test post",
            slug="test-post",
            content="This is test post content"
        )

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)

            image = models.Image.objects.create(
                post=post,
                img_file=ntf
            )

            print(image)

