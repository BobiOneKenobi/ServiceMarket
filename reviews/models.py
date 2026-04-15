from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from bookings.models import Booking
from services.models import Service

class Review(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="review",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_written",
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(
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
        return f"Review for {self.service} by {self.reviewer}"

    def clean(self):
        if not 1 <= self.rating <= 5:
            raise ValidationError({"rating": "Rating must be between 1 and 5."})

        if self.booking.status != "completed":
            raise ValidationError("Only completed bookings can be reviewed.")

        if self.reviewer != self.booking.client:
            raise ValidationError({"reviewer": "Only the client can leave a review."})

        if self.service != self.booking.service:
            raise ValidationError({"service": "Review service must match booking service."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "service"],
                name="unique_user_service_favorite",
            )
        ]

    def __str__(self):
        return f"{self.user} favorited {self.service}"