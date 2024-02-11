from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_display_links = ['title', 'publish']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug':["title"]}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name' , 'email','created']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['active', 'content', 'post__title']