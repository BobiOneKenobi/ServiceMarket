from django.contrib.auth.models import AbstractUser
from django.db import models

class MarketplaceUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(
        MarketplaceUser,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
    )
    city = models.CharField(
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
