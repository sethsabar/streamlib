

class Artist:
    def __init__(
        self,
        name: str = None,
        spotify_id: str = None,
        genres: list[str] = None
    ):
        self.name = name
        self.spotify_id = spotify_id
        self.genres = genres