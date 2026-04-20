from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Category)
class NewsDetailInline(admin.TabularInline):
    model = NewsDetail
    extra = 1
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_main', 'is_featured', 'created_at')
    list_filter = ('category', 'is_main', 'is_featured', 'is_breaking', 'is_trending')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}

    inlines = [NewsDetailInline]
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'news', 'created_at')
    search_fields = ('name', 'text')
    list_filter = ('created_at',)

admin.site.register(Contact)