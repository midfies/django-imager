from django.views.generic import TemplateView
from django.shortcuts import render
from imager_images.models import Photo
from random import randint


class HomeView(TemplateView):
    template_name = 'imagersite/home.html'

    def get_context_data(self):
        photos = Photo.public.all()
        if photos:
            random_photo_index = randint(1, len(photos)) - 1
            random_photo = photos[random_photo_index]
        else:
            random_photo = None
        return {'random_photo': random_photo}
