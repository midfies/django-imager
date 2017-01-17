from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class ImagerProfile(models.Model):
    """The library Patro and all of its attributes."""

    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
    )

    PHOTOGRAPHY_CHOICES = (
        ('NATURE', 'Nature'),
        ('URBAN', 'Urban'),
        ('PORTRAIT', 'Portrait'),
    )
    camera_type = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True,)
    website = models.CharField(max_length=255, blank=True,)
    hireable = models.BooleanField(default=True)
    travel_radius = models.DecimalField(max_digits=5, decimal_places=2)
    phone = PhoneNumberField()
    type_of_photography = models.CharField(choices=PHOTOGRAPHY_CHOICES)

    def active(self):
        return ImagerProfile.objects.filter(ImagerProfile.is_active)


@receiver(post_save, sender=User)
def make_profile_from_user(sender, instance, **kwargs):
    new_profile = ImagerProfile(user=instance)
    new_profile.save()
