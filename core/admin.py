from django.contrib import admin
from .models import Playlist, Track, TrackFeatures


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    filter_horizontal = 'tracks',


@admin.register(Track)
class TracktAdmin(admin.ModelAdmin):
    pass


@admin.register(TrackFeatures)
class TrackFeaturesAdmin(admin.ModelAdmin):
    pass
