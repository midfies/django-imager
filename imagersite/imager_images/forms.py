"""Create album/upload photo forms."""
from imager_images.models import Album, Photo
from django import forms


EXCLUDE = [
    'owner',
    'date_uploaded',
    'date_modified',
    'date_published',
]


class BaseMeta:
        """Define what should be in the form."""

        exclude = EXCLUDE
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }


class AlbumForm(forms.ModelForm):
    """Form to add new album."""

    class Meta(BaseMeta):
        """Define model and stuff."""

        model = Album


class AddPhotoForm(forms.ModelForm):
    """Form to add new photo."""

    class Meta(BaseMeta):
        """Define what should be in the form."""

        model = Photo


class EditPhotoForm(forms.ModelForm):
    """Form to add new album."""

    class Meta(BaseMeta):
        """Define what should be in the form."""

        model = Photo
        # exclude = EXCLUDE + ['photo']
