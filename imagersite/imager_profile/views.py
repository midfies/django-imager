"""Views for profile page."""
from django.contrib.auth.models import User
from django.views.generic import DetailView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from imager_profile.models import ImagerProfile
from imager_profile.forms import EditProfileForm


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
        context['userdata'] = User.objects.get(username=self.request.user)
        return context


class EditProfileView(UpdateView):
    """Update profile."""

    login_required = True
    template_name = 'imager_profile/edit_profile.html'
    success_url = reverse_lazy('profile_user')
    form_class = EditProfileForm
    model = ImagerProfile

    def get_object(self):
        """Define what profile to edit."""
        return self.request.user.profile

    def form_valid(self, form):
        """If form post is successful, set the object's owner."""
        self.object = form.save()
        self.object.user.first_name = form.cleaned_data['First Name']
        self.object.user.last_name = form.cleaned_data['Last Name']
        self.object.user.email = form.cleaned_data['Email']
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
