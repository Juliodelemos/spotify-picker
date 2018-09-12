import datetime
from django.db import models


class TrackFeatures(models.Model):
    # https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
    class Meta:
        verbose_name = 'Característica da Música'
        verbose_name_plural = 'Características das Músicas'

    acousticness = models.DecimalField(max_digits=15, decimal_places=14)
    danceability = models.DecimalField(max_digits=15, decimal_places=14)
    energy = models.DecimalField(max_digits=15, decimal_places=14)
    instrumentalness = models.DecimalField(max_digits=15, decimal_places=14)
    key = models.PositiveSmallIntegerField()
    liveness = models.DecimalField(max_digits=15, decimal_places=14)
    loudness = models.DecimalField(max_digits=15, decimal_places=12)
    mode = models.SmallIntegerField()
    speechiness = models.DecimalField(max_digits=15, decimal_places=14)
    tempo = models.DecimalField(max_digits=15, decimal_places=12)
    time_signature = models.PositiveSmallIntegerField()
    valence = models.DecimalField(max_digits=15, decimal_places=14)

    def __str__(self):
        return self.track.name

    def get_fields_names(self):
        return [
            f.name for f in TrackFeatures._meta.get_fields()
                if not f.is_relation and
                   not f.one_to_one and
                   not (f.many_to_one and f.related_model)
                   and f.name != 'id'
        ]


class Track(models.Model):
    # https://developer.spotify.com/documentation/web-api/reference/tracks/get-track/
    class Meta:
        verbose_name = 'Música'
        verbose_name_plural = 'Músicas'

    spotify_id = models.CharField(max_length=22, unique=True)
    name = models.TextField()
    duration_ms = models.PositiveIntegerField()
    features = models.OneToOneField(TrackFeatures, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def duration_time(self):
        return datetime.timedelta(milliseconds=self.duration_ms)

    @property
    def get_uri(self):
        return 'spotify:track:{}'.format(self.spotify_id)

    @property
    def get_url(self):
        return 'https://open.spotify.com/track/{}'.format(self.spotify_id)

    @property
    def get_api_url(self):
        return 'https://api.spotify.com/v1/tracks/{}'.format(self.spotify_id)


class Playlist(models.Model):
    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'

    GOSTO = 1
    NAO_GOSTO = 2
    TYPE_CHOICES = (
        (GOSTO, 'Gosto!'),
        (NAO_GOSTO, 'Não gosto!')
    )

    spotify_id = models.CharField(max_length=22)
    spotify_user_id = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    date_add = models.DateTimeField(auto_now_add=True)
    tracks = models.ManyToManyField(Track, related_name='playlists')

    def __str__(self):
        return '{} - {}'.format(self.user, self.name)

    @property
    def get_uri(self):
        return 'spotify:user:{}:playlist:{}'.format(self.spotify_user_id, self.spotify_id)

    @property
    def get_url(self):
        return 'https://open.spotify.com/playlist/{}'.format(self.spotify_id)

    @property
    def get_api_url(self):
        return 'https://api.spotify.com/v1/playlists/{}'.format(self.spotify_id)


