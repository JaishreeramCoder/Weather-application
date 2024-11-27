from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # Fields for email and password
    email = models.EmailField(
        max_length=50, blank=True
    )  # Use EmailField for better validation
    password = models.CharField(
        max_length=128, blank=True
    )  # Increase length to support hashed passwords

    # One-to-one relationship with the User model
    username = models.OneToOneField(User, on_delete=models.CASCADE)

    # Optional field for storing the user's last searched city
    last_city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username.username} Profile"


# Signal to create/update Profile when User is created/updated
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)
    instance.profile.save()
