"""Create album/upload photo forms."""
from imager_images.models import Album, Photo
from django import forms


class AddAlbumForm(forms.ModelForm):
    """Form to add new album."""

    def __init__(self, *args, **kwargs):
        """Setup the form fields."""
        super(AddAlbumForm, self).__init__(*args, **kwargs)
        self.fields["cover_photo"].queryset = self.fields['owner'].queryset.first().photos.all()
        self.fields["photos"].queryset = self.fields['owner'].queryset.first().photos.all()
        del self.fields['owner']

    class Meta:
        """Define model and stuff."""

        model = Album
        exclude = [
            'date_uploaded',
            'date_modified',
            'date_published',
        ]


class EditAlbumForm(forms.ModelForm):
    """Form to add new album."""

    class Meta:

        model = Album
        exclude = [
            'owner',
            'date_uploaded',
            'date_modified',
            'date_published',
        ]


class AddPhotoForm(forms.ModelForm):
    """Form to add new photo."""

    def __init__(self, *args, **kwargs):
        """Setup the form fields."""
        super(AddPhotoForm, self).__init__(*args, **kwargs)
        self.fields["photo"].queryset = self.fields['owner'].queryset.first().photos.all()
        del self.fields['owner']

    class Meta:
        """Define what should be in the form."""

        model = Photo
        exclude = [
            'date_uploaded',
            'date_modified',
            'date_published',
        ]


class EditPhotoForm(forms.ModelForm):
    """Form to add new album."""

    class Meta:

        model = Photo
        exclude = [
            'owner',
            'date_uploaded',
            'date_modified',
            'date_published',
            'photo'
        ]