"""Views for profile page."""
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.views.generic import DetailView, TemplateView


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


class ProfileUserView(TemplateView):
    """"ProfileView."""

    template_name = 'imager_profile/profile.html'
    model = ImagerProfile

    def get_context_data(self, **kwargs):
        """Get profile information and return it."""
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        profile = ImagerProfile.active.get(user__username=self.request.user)
        context['profile'] = profile
        context['userdata'] = User.objects.filter(username=self.request.user).first()
        return context
