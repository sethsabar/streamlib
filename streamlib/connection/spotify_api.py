from requests import Session
from ..objects import Song, Artist, Album


class SpotifyAPI:

    def __init__(self):
        """
        an wrapper object for the Spotify API, this should not be accessed 
        directly
        """
        self._session = Session()
        self._base_url = "https://api.spotify.com/v1/"
    
    def _get_song_by_id(self, id: str, token: str) -> Song:
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
            headers=headers).json()
        
        if 'error' in res:
            message = "Spotify API failed to retrieve song with id " + str(id) \
            + " because of the following error: " + str(res['error'])
            raise RuntimeError(message)
        else:
            return self._create_song(res)

    def _create_song(self, json) -> Song:
        album_obj = json['album']
        artists_list = json['artists']
        artists = []
        for a in artists_list:
            artists.append(Artist(
                name=a['name'],
                spotify_id=a['id']
            ))
        album = Album(
            name=album_obj['name'],
            spotify_id=album_obj['id'],
            release_date=album_obj['release_date'],
            release_date_precision=album_obj['release_date_precision'],
            album_type=album_obj['type']
        )
        return Song(
            name=json['name'],
            spotify_id=json['id'],
            duration=json['duration_ms'],
            explicit=json['explicit'],
            albums=[album],
            artists=artists,
        )

    def _create_songs(self, json):
        return [self._create_song(li) for li in json]

    def _get_songs_by_id(self, ids: list[str], token: str) -> list[Song]:
        """
        given a list of song ids and an access token, calls the API and with 
        the returned JSON creates a list of Song objects
        """
        if len(ids) == 0:
            return []
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }
        res = self._session.get(
            url="{}tracks/?ids={}".format(self._base_url, ','.join(ids)),
            headers=headers).json()
        
        if 'error' in res:
            message = "Spotify API failed to retrieve songs with ids " \
            + str(ids) + " because of the following error: " + str(res['error'])
            raise RuntimeError(message)
        else:
            return self._create_songs(res['tracks'])

    def _get_saved_songs(self, token: str) -> Song:
        """
        gets saved songs for Spotify user
        """
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }
        res = self._session.get(
            url="{}me/tracks".format(self._base_url),
            headers=headers).json()
        
        if 'error' in res:
            message = "Spotify API failed to retrieve song with id " + str(id) \
            + " because of the following error: " + str(res['error'])
            raise RuntimeError(message)
        else:
            ret_list = \
            self._create_songs(item['track'] for item in res['items'])
            while (next := res['next']) is not None:
                ret_list.append(self._create_songs(res['items']))
                res = self._session.get(
                    url=next,
                    headers=headers).json()
            return ret_list

