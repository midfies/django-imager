"""Models for the imager_images app."""

from django.db import models
from imager_profile.models import ImagerProfile


class Photo(models.Model):
    """The Photo model and all of its attributes."""

    owner = models.ForeignKey(
        ImagerProfile,
        related_name='photos',
        on_delete=models.CASCADE,
    )

    PUBLISH_CHOICES = (
        ('PRIVATE', 'Private'),
        ('SHARED', 'Shared'),
        ('PUBLIC', 'Public'),
    )

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)
    published = models.CharField(max_length=144,
                                 choices=PUBLISH_CHOICES,
                                 default='PRIVATE')
    photo = models.ImageField(upload_to='', blank=True, null=True)


class Album(models.Model):
    """The Album model and all of its attributes."""

    owner = models.ForeignKey(
        ImagerProfile,
        related_name='albums',
        on_delete=models.CASCADE,
    )

    photos = models.ManyToManyField(
        Photo,
        related_name='albums'
    )

    PUBLISH_CHOICES = (
        ('PRIVATE', 'Private'),
        ('SHARED', 'Shared'),
        ('PUBLIC', 'Public'),
    )

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)
    published = models.CharField(max_length=144,
                                 choices=PUBLISH_CHOICES,
                                 default='PRIVATE')
    cover_photo = models.ImageField(upload_to='', blank=True, null=True)
