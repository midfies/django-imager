from django.shortcuts import render
from django.http import Http404
from imager_profile.models import ImagerProfile
from imager_images.models import Album, Photo

# Create your views here.


def library_view(request):
    """."""
    try:
        profile = ImagerProfile.active.get(user__username=request.user.username)
        photos = profile.photos.all()
        albums = profile.albums.all()
        username = request.user.username
        return render(request, 'imager_images/library.html', {'photos': photos, 'profile': profile, 'albums': albums, 'username': username})
    except ImagerProfile.DoesNotExist:
        raise Http404("No MyModel matches the given query.")


def album_view(request, albumid):
    """."""
    album = Album.public.get(id=albumid)
    photos = album.photos.all()
    return render(request, 'imager_images/album.html', {'album': album, 'photos': photos})


def photo_view(request, photoid):
    """."""
    photo = Photo.public.filter(id=photoid).first()
    return render(request, 'imager_images/photo.html', {'photo': photo})


def photo_gallery_view(request):
    """."""
    photos = Photo.public.all()
    return render(request, 'imager_images/photo_gallery.html', {'photos': photos})


def album_gallery_view(request):
    """."""
    albums = Album.public.all()

    return render(request, 'imager_images/album_gallery.html', {'albums': albums})
