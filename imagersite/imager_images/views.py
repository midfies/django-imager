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
    album = Album.objects.get(id=albumid)
    photos = album.photos.all()
    return render(request, 'imager_images/album.html', {'album': album, 'photos': photos})
