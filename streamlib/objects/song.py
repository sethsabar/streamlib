from streamlib.objects.album import Album
from streamlib.objects.artist import Artist

class Song:
    def __init__(
        self,
        name: str = None,
        artists: list[Artist] = None,
        album: Album = None,
        spotify_id: str = None,
        duration_ms: int = None,
        explicit: bool = None,
        song_number: int = None,
        spotify_is_local: bool = None
        ):
        self.name = name
        self.artists = artists
        self.album = album
        self.duration_ms = duration_ms
        self.spotify_id = spotify_id
        self.explicit = explicit
        self.song_number = song_number
        self.spotify_is_local = spotify_is_local
