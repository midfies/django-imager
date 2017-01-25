"""Views for profile page."""
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.views.generic import TemplateView


class ProfileView(TemplateView):
    """"ProfileView."""

    template_name = 'imager_profile/profile.html'

    def get_context_data(self, username):
        """Get albums and photos and return them."""
        if username == "USER":
            username = self.request.user.username
        profile = ImagerProfile.active.get(user__username=username)
        user = User.objects.filter(username=username).first()
        photos = profile.photos.all()
        return {'photos': photos, 'profile': profile, 'userdata': user}
