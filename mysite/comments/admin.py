from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
    date_hierarchy = 'created_at'
