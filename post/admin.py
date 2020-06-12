from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Tag, Image
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class TagResource(resources.ModelResource):

    class Meta:
        model = Tag

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'get_tags', 'status', 'created_on')
    # list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    def get_tags(self, obj):
        return ",".join([tag.title for tag in obj.tag.all()])
    get_tags.short_description = "TAGS"
    

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Comment, CommentAdmin)

class TagAdmin(ImportExportModelAdmin):
    list_display = ('title', 'created_on')
    prepopulated_fields = {'slug': ('title', )}
    resource_class = TagResource

admin.site.register(Tag, TagAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'created_on', 'post')
    # prepopulated_fields = {'slug': ('title', )}

    def image_tag(self, obj):
        return format_html('<img src="{}"/>'.format(obj.img_file.url))
    
    image_tag.short_description = "Image"

admin.site.register(Image, ImageAdmin)
