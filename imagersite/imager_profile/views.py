"""Views for profile page."""
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.views.generic import DetailView


class ProfileView(DetailView):
    """"ProfileView."""
    template_name = 'imager_profile/profile.html'

    def get_queryset(self):
        """Redefining because I have to."""
        if self.kwargs['username']:
            username = self.kwargs['username']
        else:
            username = self.request.user.username
        return ImagerProfile.active.get(user__username=username)
    #     profile = ImagerProfile.active.get(user__username=username)
    # def get_context_data(self, username):
    #     """Get albums and photos and return them."""
    #     if username == "USER":
    #         username = self.request.user.username
    #     profile = ImagerProfile.active.get(user__username=username)
    #     user = User.objects.filter(username=username).first()
    #     photos = profile.photos.all()
    #     return {'photos': photos, 'profile': profile, 'userdata': user}
