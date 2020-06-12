from ..models import Post, Tag, Image
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title', 'slug']

class ImageSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()

    def get_url(self, obj):        
        return str(obj)

    class Meta:
        model = Image
        fields = ["url"]
        
class PostSerializer(serializers.ModelSerializer):
    # Rất vô lí tag, image phải có s mới chạy được.
    tags = TagSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['images', 'tags', 'title', 'slug', 'content', 'created_on']