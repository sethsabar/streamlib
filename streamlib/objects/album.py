
class Album:
    def __init__(
        self,
        name: str = None,
        artists: list = None,
        songs: list = None,
        album_type: str = None,
        spotify_id: str = None,
        release_date: str = None,
        release_date_precision: str = None
    ):
        self._name = name
        self._artists = artists
        self._songs = songs
        self._album_type = album_type
        self._spotify_id = spotify_id
        self._release_date = release_date
        self.release_date_precision = release_date_precision
