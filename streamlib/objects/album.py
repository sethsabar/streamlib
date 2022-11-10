
class Album:
    def __init__(
        self,
        name: str = None,
        artists: list = None,
        songs: list = None,
        num_songs: int = None,
        spotify_album_type: str = None,
        spotify_id: str = None,
        release_year: int = None,
        release_month: int = None,
        release_day: int = None,
        disc_number: int = None
    ):
        self.name = name
        self.artists = artists
        self.songs = songs
        self.num_songs = num_songs
        self.spotify_album_type = spotify_album_type
        self.spotify_id = spotify_id
        self.release_year = release_year
        self.release_month = release_month
        self.realase_day = release_day
        self.disc_number = disc_number