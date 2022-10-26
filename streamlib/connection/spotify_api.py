from requests import Session


class SpotifyAPI:

    def __init__(self):
        """
        an wrapper object for the Spotify API, this should not be accessed 
        directly
        """
        self._session = Session()
        self._base_url = "https://api.spotify.com/v1/"

    def _get_song_by_id(self, id, token):
        """
        given a song id and an access token, calls the API and with the 
        returned JSON creates a Song object 
        """
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }
        res = self._session.get(
            url="{}tracks/{}".format(self._base_url, id),
            headers=headers)
        print(res.json())

