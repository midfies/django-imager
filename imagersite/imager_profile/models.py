from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from django.db.models.signals import post_save
from django.dispatch import receiver


class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return super(ActiveUserManager, self).get_queryset().filter(user__is_active=True)


class ImagerProfile(models.Model):
    """The library Patro and all of its attributes."""

    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
    )

    active = ActiveUserManager()

    PHOTOGRAPHY_CHOICES = (
        ('NATURE', 'Nature'),
        ('URBAN', 'Urban'),
        ('PORTRAIT', 'Portrait'),
    )
    camera_type = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    hireable = models.BooleanField(default=True)
    travel_radius = models.DecimalField(max_digits=5,
                                        decimal_places=2,
                                        null=True)
    phone = PhoneNumberField()
    type_of_photography = models.CharField(max_length=144,
                                           choices=PHOTOGRAPHY_CHOICES)


@receiver(post_save, sender=User)
def make_profile_from_user(sender, instance, **kwargs):
    if kwargs['created']:
        profile = ImagerProfile(user=instance)
    else:
        profile = instance
    profile.save()
