"""Views for albums and photos."""
from imager_profile.models import ImagerProfile
from imager_images.models import Album, Photo
from django.views.generic import ListView, TemplateView

# Create your views here.


class LibraryView(ListView):
    """"LibraryView."""

    template_name = 'imager_images/library.html'

    def get_context_data(self):
        """Get albums and photos and return them."""
        profile = ImagerProfile.active.get(user__username=self.request.user.username)
        photos = profile.photos.all()
        albums = profile.albums.all()
        username = self.request.user.username
        return {'photos': photos, 'profile': profile, 'albums': albums, 'username': username}

    def get_queryset(self):
        """Redefining because I have to."""
        return {}


class AlbumView(TemplateView):
    """"AlbumView."""

    template_name = 'imager_images/album.html'
    model = Album

    def get_context_data(self, albumid):
        """Get albums and photos and return them."""
        album = Album.public.get(id=albumid)
        photos = album.photos.all()
        return {'album': album, 'photos': photos}

    def get_queryset(self):
        """Redefining because I have to."""
        return {}


class AlbumGalleryView(ListView):
    """"AlbumGalleryView."""

    template_name = 'imager_images/album_gallery.html'

    def get_context_data(self):
        """Get all public albums return them."""
        albums = Album.public.all()
        return {'albums': albums}

    def get_queryset(self):
        """Redefining because I have to."""
        return {}


class PhotoGalleryView(ListView):
    """"PhotoGalleryView."""

    template_name = 'imager_images/photo_gallery.html'

    def get_context_data(self):
        """Get all public photos and return them."""
        photos = Photo.public.all()
        return {'photos': photos}

    def get_queryset(self):
        """Redefining because I have to."""
        return {}
