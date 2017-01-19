from django.contrib import admin
from imager_images.models import Photo, Album


# class PhotoAdmin(admin.ModelAdmin):
#     list_display = ("title", "description")
#     fields = ('title',
#               'description',
#               'published',
#               'owner')


# class AlbumAdmin(admin.ModelAdmin):
#     list_display = ("title", "description")
#     filter_horizontal = ('photos',)
#     fields = ('title',
#               'description',
#               'published',
#               'owner')

admin.site.register(Photo)


class AlbumInline(admin.TabularInline):
    model = Album.photos.through


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = (AlbumInline,)
    exclude = ('photos',)
