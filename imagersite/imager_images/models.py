"""Models for the imager_images app."""

from django.db import models
from imager_profile.models import ImagerProfile


class PublicPhotosManger(models.Manager):
    """Active user manager."""

    def get_queryset(self):
        """Get the query set of public photos."""
        return super(PublicPhotosManger, self).get_queryset().filter(published="PUBLIC")


class Photo(models.Model):
    """The Photo model and all of its attributes."""

    objects = models.Manager()
    public = PublicPhotosManger()

    owner = models.ForeignKey(
        ImagerProfile,
        related_name='photos',
        on_delete=models.CASCADE,
        blank=True,
        null=True
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


class PublicAlbumManger(models.Manager):
    """Active user manager."""

    def get_queryset(self):
        """Get the query set of public photos."""
        return super(PublicAlbumManger, self).get_queryset().filter(published="PUBLIC")


class Album(models.Model):
    """The Album model and all of its attributes."""

    objects = models.Manager()
    public = PublicAlbumManger()

    owner = models.ForeignKey(
        ImagerProfile,
        related_name='albums',
        on_delete=models.CASCADE,
        blank=True,
        null=True
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
    cover_photo = models.ForeignKey(Photo, blank=True, null=True, related_name="+")
