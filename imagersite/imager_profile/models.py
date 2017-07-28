from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from django.db.models.signals import post_save
from django.dispatch import receiver


class ActiveUsersManger(models.Manager):
    """Active user manager."""

    def get_queryset(self):
        """Get the query set of active users."""
        return super(ActiveUsersManger, self).get_queryset().filter(user__is_active=True)


class ImagerProfile(models.Model):
    """The library Patro and all of its attributes."""

    objects = models.Manager()
    active = ActiveUsersManger()

    user = models.OneToOneField(User,
                                related_name='profile',
                                on_delete=models.CASCADE)
    camera_type = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    hireable = models.BooleanField(default=True)
    travel_radius = models.DecimalField(max_digits=5,
                                        decimal_places=2,
                                        null=True)
    phone = PhoneNumberField()
    type_of_photography = models.CharField(max_length=144,
                                           blank=True,
                                           null=True)

    @property
    def is_active(self):
        """Return if user of profile is active."""
        return self.user.is_active

    def __str__(self):
        """Return string representation of model instance."""
        return str(self.user.username)


@receiver(post_save, sender=User)
def make_profile_from_user(sender, instance, **kwargs):
    """When a user is created, they get a profile."""
    if kwargs['created']:
        profile = ImagerProfile(user=instance)
        profile.save()
