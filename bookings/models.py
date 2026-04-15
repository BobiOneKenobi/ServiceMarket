from datetime import date
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from services.models import Service

class AvailabilitySlot(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="availability_slots",
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.service.title} - {self.date} {self.start_time}-{self.end_time}"

    def clean(self):
        if self.date < date.today():
            raise ValidationError({"date": "You cannot create a slot in the past."})

        if self.end_time <= self.start_time:
            raise ValidationError(
                {"end_time": "End time must be later than start time."}
            )

        overlapping_slots = AvailabilitySlot.objects.filter(
            service=self.service,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )

        if self.pk:
            overlapping_slots = overlapping_slots.exclude(pk=self.pk)

        if overlapping_slots.exists():
            raise ValidationError("This slot overlaps with an existing slot.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("rejected", "Rejected"),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    slot = models.OneToOneField(
        AvailabilitySlot,
        on_delete=models.PROTECT,
        related_name="booking",
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings_made",
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings_received",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    client_message = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client} -> {self.service} ({self.status})"

    def clean(self):
        if self.client == self.service.owner:
            raise ValidationError("You cannot book your own service.")

        if self.provider != self.service.owner:
            raise ValidationError({"provider": "Provider must be the service owner."})

        if self.slot.service != self.service:
            raise ValidationError({"slot": "Selected slot does not belong to this service."})

        if self.slot.is_booked and not self.pk:
            raise ValidationError({"slot": "This slot has already been booked."})

    def save(self, *args, **kwargs):
        self.provider = self.service.owner
        self.full_clean()
        super().save(*args, **kwargs)
