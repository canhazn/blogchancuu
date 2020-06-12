from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django_unique_slugify import unique_slugify
from django.utils import timezone

STATUS = (
	(0, "Draft"),
	(1, "Publish")
)

class Tag(models.Model):
	title = models.CharField(max_length=200, null=True, blank=False)
	slug = models.SlugField(max_length=200, null=True, blank=False)
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

class Post(models.Model):
	title = models.CharField(max_length=200, null=True, blank=True)
	slug  = models.SlugField(max_length=200, null=True, blank=True)
	# author = models.ForeignKey(User, on_delete= models.CASCADE, related_name="blog_posts")
	update_on = models.DateTimeField(auto_now= True)
	content = models.TextField(null=True, blank=True)
	created_on = models.DateTimeField(auto_now_add= True)
	# created_on = models.DateTimeField(editable=False, default=timezone.now)
	status = models.IntegerField(choices= STATUS, default=1)
	tags = models.ManyToManyField(Tag, blank=True)

	class Meta:
		ordering = ['-created_on']

	def __str__(self):
		return self.slug

	def save(self, **kwargs):
		# check because update post can overwrite slug
		if not self.slug:			
			slug_str = "%s" % (timezone.now()) 				
			unique_slugify(self, slug_str) 
		
		super(Post, self).save(**kwargs)

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ['created_on']

	def __str__(self):
		return 'Comment {} by {}'.format(self.body, self.name)

def path_file_name(instance, filename):
	return "/".join(filter(None, (instance.post.slug, filename)))

class Image(models.Model): 
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
	created_on = models.DateTimeField(auto_now_add=True)
	img_file = models.ImageField(upload_to=path_file_name, null=True, blank=True)

	def __str__(self):
		return self.img_file.url