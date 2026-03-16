from django.contrib import admin
from .models import Loader, Category, Content, ContentVersion, Screenshot, Theme, Report

class ContentVersionInline(admin.TabularInline):
    model = ContentVersion
    extra = 0

class ScreenshotInline(admin.TabularInline):
    model = Screenshot
    extra = 0

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'downloads', 'is_approved', 'is_featured', 'created_at']
    list_filter = ['is_approved', 'is_featured', 'category', 'loaders']
    list_editable = ['is_approved', 'is_featured']
    search_fields = ['title', 'description', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ContentVersionInline, ScreenshotInline]
    filter_horizontal = ['loaders']

@admin.register(Loader)
class LoaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['content', 'reporter', 'reason', 'created_at', 'resolved']
    list_editable = ['resolved']
    list_filter = ['reason', 'resolved']