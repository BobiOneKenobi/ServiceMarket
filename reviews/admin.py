from django.contrib import admin
from .models import Favorite, Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("service", "reviewer", "rating", "created_at")
    list_filter = ("rating", "created_at")

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "created_at")