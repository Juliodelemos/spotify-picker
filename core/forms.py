from decimal import Decimal

from spotipy.client import SpotifyException

from django import forms
from django.db import transaction

from .models import Playlist, Track, TrackFeatures
from .spotify_connection import SpotifyConnection


class AddPlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = 'type', 'uri'

    uri = forms.CharField(max_length=70)
    playlist = None
    sp = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        c = self.cleaned_data
        username = self.cleaned_data['uri'].split(':')[2]
        playlist_id = self.cleaned_data['uri'].split(':')[4]

        if Playlist.objects.filter(user=self.user, spotify_id=playlist_id).exists():
            raise forms.ValidationError('Você já importou esta playlist.')

        self.sp = SpotifyConnection().get_client()
        try:
            self.playlist = self.sp.user_playlist(username, playlist_id)
        except SpotifyException:
            self.add_error('uri', 'Playlist não encontrada.')
        return c

    def save(self, commit=True):
        playlist = super().save(commit=False)

        with transaction.atomic():
            playlist.spotify_id = self.playlist['id']
            playlist.spotify_user_id = self.playlist['owner']['id']
            playlist.name = self.playlist['name']
            playlist.description = self.playlist['description']
            playlist.user = self.user
            playlist.save()

            # Carregando as tracks da playlist
            all_tracks = {}
            new_tracks = {}
            for t in self.playlist['tracks']['items']:
                t = t['track']
                track = Track.objects.filter(spotify_id=t['id']).first()
                if track is None:
                    track = Track(spotify_id=t['id'], duration_ms=t['duration_ms'], name=t['name'])
                    new_tracks[t['id']] = track
                all_tracks[track.spotify_id] = track

            # Extrando somente os IDs das músicas novas
            new_tracks_ids = [t.spotify_id for t in new_tracks.values()]

            # Pegando as features de todas as tracks novas com um só request
            if new_tracks:
                features = self.sp.audio_features(new_tracks_ids)
                for feature in features:
                    track = new_tracks[feature['id']]
                    track_features = TrackFeatures()
                    for field in track_features.get_fields_names():
                        if isinstance(feature[field], float):
                            # Para gantir a precisão do valor decimal
                            setattr(track_features, field, Decimal(str(feature[field])))
                        else:
                            setattr(track_features, field, feature[field])
                    track_features.save()
                    track.features = track_features
                    track.save()

            # Relacionando as tracks com a playlist
            playlist.tracks.add(*list(all_tracks.values()))

            if commit:
                playlist.save()
        return playlist
