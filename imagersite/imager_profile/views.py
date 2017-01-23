from django.shortcuts import render
from imager_profile.models import ImagerProfile


def profile_view(request, username):
    """."""
    profile = ImagerProfile.active.get(user__username=username)
    photos = profile.photos.all()
    return render(request, 'imager_profile/profile.html', {'photos': photos})