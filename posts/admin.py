from django.contrib import admin
from .models import Post, Comment, Vote, UserProfile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'score', 'created_at', 'comment_count']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'url']
    readonly_fields = ['score', 'created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content_preview', 'author', 'post', 'parent', 'score', 'created_at']
    list_filter = ['created_at', 'author']
    readonly_fields = ['score', 'created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'karma', 'created_at']
    readonly_fields = ['karma', 'created_at']
