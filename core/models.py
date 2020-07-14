from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Tag(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, null=False, blank=False)

    def __str__(self):
        return str(self.slug)


class Post(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    update_on = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.slug)

    def save(self, *args, **kwargs):
        # check because update post can overwrite slug
        if not self.slug:
            slug_str = slugify(timezone.now())
            self.slug = slug_str

        super().save(*args, **kwargs)
