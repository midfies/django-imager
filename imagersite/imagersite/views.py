from django.shortcuts import render
from imager_images.models import Photo
from random import randint


def home_view(request):
    """."""
    photos = Photo.public.all()
    if photos:
        random_photo_index = randint(1, len(photos)) - 1
        random_photo = photos[random_photo_index]
    else:
        random_photo = None
    return render(request,
                  'imagersite/home.html',
                  {'random_photo': random_photo})
