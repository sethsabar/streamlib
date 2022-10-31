

class Artist:
    def __init__(
        self,
        name: str = None,
        spotify_id: str = None,
    ):
        self._name = name
        self._spotify_id = spotify_id