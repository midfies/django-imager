from imager_images.models import Album, Photo
from django import forms


class AddAlbumForm(forms.ModelForm):
    """Form to add new album."""

    class Meta:
        """Define model and stuff."""

        model = Album
        exclude = []


class AddPhotoForm(forms.ModelForm):
    """Form to add new photo."""

    class Meta:
        """Define what should be in the form."""

        model = Photo
        exclude = []
