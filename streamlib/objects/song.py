from .artist import Artist
from .album import Album

class Song:
    def __init__(
        self,
        name: str = None,
        artists: list[Artist] = None,
        albums: list[Album] = None,
        spotify_id: str = None,
        duration: int = None,
        explicit: bool = None):
        self._name = name
        self._artists = artists
        self._albums = albums
        self._duration = duration
        self._spotify_id = spotify_id
        self._explicit = explicit
