from django.contrib import admin
from import_export import resources
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin

from core.models import Post, Image, Tag


class PostResource(resources.ModelResource):
    class Meta:
        model = Post


class PostAdmin(SummernoteModelAdmin, ImportExportModelAdmin):
    summernote_fields = ('content',)
    list_display = ('slug', 'title', 'get_tags', 'get_content')
    # list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    resource_class = PostResource

    def get_tags(self, obj):
        return ",".join([tag.title for tag in obj.tags.all()])
    get_tags.short_description = "TAGS"

    def get_content(self, obj):
        return format_html("<div style='overflow: hidden; text-overflow: ellipsis;'>{}</div>".format(obj.content))
    get_content.short_description = "CONTENTS"


admin.site.register(Post, PostAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Tag, TagAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'post']
    # prepopulated_fields = {'slug': ('title', )}

    def image_tag(self, obj):
        return format_html('<img style="max-width: 400px" src="{}"/>'.format(obj.img_file.url))

    image_tag.short_description = "Image"


admin.site.register(Image, ImageAdmin)
