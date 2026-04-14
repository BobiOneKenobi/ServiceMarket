from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MarketplaceUser, Profile

@admin.register(MarketplaceUser)
class MarketplaceUserAdmin(UserAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city")
    search_fields = ("user__username", "user__email", "city")