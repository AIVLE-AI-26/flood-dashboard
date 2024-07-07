from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'views', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'content')


