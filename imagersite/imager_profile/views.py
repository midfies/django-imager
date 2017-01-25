"""Views for profile page."""
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.views.generic import DetailView


class ProfileView(DetailView):
    """"ProfileView."""
    template_name = 'imager_profile/profile.html'
    model = ImagerProfile
    slug_field = 'user__username'
    def get_context_data(self, **kwargs):
        """Get profile information and return it."""
        context = super(ProfileView, self).get_context_data(**kwargs)
        profile = ImagerProfile.active.get(user__username=self.kwargs['slug'])
        context['profile'] = profile
        context['userdata'] = User.objects.filter(username=self.kwargs['slug']).first()
        return context
