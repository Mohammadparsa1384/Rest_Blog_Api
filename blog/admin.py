from django.contrib import admin
from .models import (Post, Category, Tag, Comment)

# Register yourm models here
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_date')
    list_filter = ('status', 'created_date', 'category', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['author','category', 'tags']
    date_hierarchy = 'created_date'
    ordering = ('-created_date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'content','author', 'created_date', 'is_approved')
    list_filter = ('is_approved', 'created_date') 
    search_fields = ('author__user__email', 'content', 'post__title')  # Searchable fields
    actions = ['approve_comments']  # Custom admin action
    
    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)