from django.shortcuts import render
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile


def profile_view(request, username):
    """."""
    if username == "USER":
        username = request.user.username
    profile = ImagerProfile.active.filter(user__username=username).first()
    user = User.objects.filter(username=username).first()
    photos = profile.photos.all()
    return render(request, 'imager_profile/profile.html', {'photos': photos, 'profile': profile, 'userdata': user})
