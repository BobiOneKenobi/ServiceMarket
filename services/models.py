from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
    )
    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ("online", "Online"),
        ("on_site", "On-site"),
        ("both", "Both"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="services",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="services",
    )
    title = models.CharField(
        max_length=120,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
    )
    short_description = models.CharField(
        max_length=180,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
    )
    location = models.CharField(
        max_length=120,
        blank=True,
    )
    estimated_duration_minutes = models.PositiveIntegerField()
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="services",
    )
    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(
        default=True,
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
        return self.title

    def clean(self):
        if self.price < 0:
            raise ValidationError({"price": "Price cannot be negative."})

        if self.estimated_duration_minutes <= 0:
            raise ValidationError(
                {"estimated_duration_minutes": "Duration must be greater than 0."}
            )

        if self.service_type == "on_site" and not self.location:
            raise ValidationError(
                {"location": "Location is required for on-site services."}
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.full_clean()
        super().save(*args, **kwargs)