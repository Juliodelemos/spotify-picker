import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings


class SpotifyConnection(object):
    __spotify = None

    def __get_client(self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=settings.SPOTIPY_CLIENT_ID,
            client_secret=settings.SPOTIPY_CLIENT_SECRET
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_client(self):
        if self.__spotify is None:
            self.__spotify = self.__get_client()
        return self.__spotify