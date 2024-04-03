from django.contrib import admin

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_filter = ('title',)
    search_fields = ('title', 'content')
