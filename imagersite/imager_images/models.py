"""Models for the imager_images app."""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from easy_thumbnails.fields import ThumbnailerImageField
from taggit.managers import TaggableManager

from imager_profile.models import ImagerProfile


class PublicManager(models.Manager):
    """Active user manager."""

    def get_queryset(self):
        """Get the query set of public photos."""
        return super(PublicManager, self).get_queryset().filter(published="PUBLIC")


@python_2_unicode_compatible
class BaseItem(models.Model):
    """Common model to photos and albums."""

    class Meta:
        """Set default ordering."""

        ordering = ['date_uploaded']
        abstract = True

    objects = models.Manager()
    public = PublicManager()
    title = models.CharField(max_length=128)
    owner = models.ForeignKey(ImagerProfile,
                              null=True,
                              on_delete=models.CASCADE,
                              related_name="%(class)ss")
    PUBLISH_CHOICES = (('PRIVATE', 'Private'),
                       ('PUBLIC', 'Public'))
    published = models.CharField(max_length=144,
                                 choices=PUBLISH_CHOICES,
                                 default='PRIVATE')
    date_modified = models.DateTimeField(auto_now=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        """Return readable representation."""
        return self.title


@python_2_unicode_compatible
class Photo(BaseItem):
    """Photo model."""

    photo = ThumbnailerImageField(upload_to='')
    tags = TaggableManager(blank=True)


@python_2_unicode_compatible
class Album(BaseItem):
    """Album model."""

    cover_photo = models.ForeignKey(Photo,
                                    related_name="+",
                                    null=True)
    photos = models.ManyToManyField(Photo,
                                    related_name='albums')
