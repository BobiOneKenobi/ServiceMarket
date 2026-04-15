from django.contrib import admin
from .models import AvailabilitySlot, Booking

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("service", "date", "start_time", "end_time", "is_booked")
    list_filter = ("date", "is_booked")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("service", "client", "provider", "status", "created_at")
    list_filter = ("status", "created_at")