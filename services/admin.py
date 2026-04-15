from django.contrib import admin
from .models import Category, Service, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "price", "service_type", "is_published")
    list_filter = ("category", "service_type", "is_published")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}