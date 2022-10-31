from streamlib.objects.album import Album
from streamlib.objects.artist import Artist

class Song:
    def __init__(
        self,
        name: str = None,
        artists: list[Artist] = None,
        album: Album = None,
        spotify_id: str = None,
        duration: int = None,
        explicit: bool = None):
        self._name = name
        self._artists = artists
        self._album = album
        self._duration = duration
        self._spotify_id = spotify_id
        self._explicit = explicit
