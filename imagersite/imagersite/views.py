from django.shortcuts import render
from imager_profile.models import ImagerProfile
from random import randint


def home_view(request):
    """."""
    profile = ImagerProfile.active.filter(user__username=request.user.username).first()
    photos = profile.photos.all()
    if photos:
        random_photo_index = randint(1, len(photos)) - 1
        random_photo = photos[random_photo_index]
    else:
        random_photo = None
    return render(request, 'imagersite/home.html',
                        {
                        'random_photo': random_photo,
                        }
                    )

