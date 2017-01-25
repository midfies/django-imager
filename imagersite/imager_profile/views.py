"""Views for profile page."""
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.views.generic import TemplateView


class ProfileView(TemplateView):
    """"ProfileView."""

    template_name = 'imager_profile/profile.html'
    model = ImagerProfile

    def get_context_data(self, **kwargs):
        """Get profile information and return it."""
        context = super(ProfileView, self).get_context_data(**kwargs)
        profile = ImagerProfile.active.get(user__username=self.kwargs['username'])
        context['profile'] = profile
        context['userdata'] = User.objects.filter(username=self.kwargs['username']).first()
        return context
