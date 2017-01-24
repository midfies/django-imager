from django.shortcuts import render
from imager_profile.models import ImagerProfile
from imager_images.models import Album, Photo

# Create your views here.


def library_view(request):
    """."""
    profile = ImagerProfile.active.filter(user__username=request.user.username).first()
    photos = profile.photos.all()
    albums = profile.albums.all()
    username = request.user.username
    return render(request, 'imager_images/library.html', {'photos': photos, 'profile': profile, 'albums': albums, 'username': username})


def album_view(request, albumid):
    """."""
    album = Album.public.filter(id=albumid).first()
    photos = album.photos.all()
    return render(request, 'imager_images/album.html', {'album': album, 'photos': photos})


def photo_view(request, photoid):
    """."""
    photo = Photo.public.filter(id=photoid).first()
    return render(request, 'imager_images/photo.html', {'photo': photo})
