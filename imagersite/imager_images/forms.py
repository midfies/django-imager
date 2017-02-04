"""Create album/upload photo forms."""
from imager_images.models import Album, Photo
from django import forms


class AddAlbumForm(forms.ModelForm):
    """Form to add new album."""

    class Meta:
        """Define model and stuff."""

        model = Album
        exclude = [
            'date_uploaded',
            'date_modified',
            'date_published',
            'owner'
        ]


class EditAlbumForm(forms.ModelForm):
    """Form to add new album."""

    class Meta:
        """Define the model and exclude fields."""

        model = Album
        exclude = [
            'owner',
            'date_uploaded',
            'date_modified',
            'date_published',
            'owner'
        ]


class AddPhotoForm(forms.ModelForm):
    """Form to add new photo."""

    class Meta:
        """Define what should be in the form."""

        model = Photo
        exclude = [
            'owner',
            'date_uploaded',
            'date_modified',
            'date_published',
        ]


class EditPhotoForm(forms.ModelForm):
    """Form to add new album."""

    class Meta:
        """Define what should be in the form."""

        model = Photo
        exclude = [
            'owner',
            'date_uploaded',
            'date_modified',
            'date_published',
            'photo'
        ]
