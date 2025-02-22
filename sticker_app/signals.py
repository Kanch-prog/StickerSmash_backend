from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import AdminProfile  # Use AdminProfile now

@receiver(post_save, sender=User)
def create_admin_profile(sender, instance, created, **kwargs):
    if created:
        AdminProfile.objects.create(user=instance)  # Create AdminProfile for new users

@receiver(post_save, sender=User)
def save_admin_profile(sender, instance, **kwargs):
    instance.adminprofile.save()  # Save AdminProfile when User is saved
