from json import JSONDecodeError
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
    
    def _gen_header(self, token: str) -> dict[str, str]:
        return {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }
    
    def _get_song_by_id(self, id: str, token: str) -> Song:
        """
        given a song id and an access token, calls the API and with the 
        returned JSON creates a Song object 
        """
        res = self._session.get(
            url="{}tracks/{}".format(self._base_url, id),
            headers=self._gen_header(token)).json()
        
        if 'error' in res:
            message = "Spotify API failed to retrieve song with id " + str(id) \
            + " because of the following error: " + str(res['error'])
            raise RuntimeError(message)
        else:
            return self._create_song(res)
    
    def _parse_album_release(self, date: str, precision: str) -> \
    tuple[int, int, int]:
        date_list = date.split('-')
        if precision == 'year':
            return int(date_list[0]), None, None
        elif precision == 'month':
            return int(date_list[0]), int(date_list[1]), None 
        else:
            return int(date_list[0]), int(date_list[1]), int(date_list[2]) 

    def _create_song(self, json) -> Song:
        album_obj = json['album']
        artists_list = json['artists']
        artists = []
        for a in artists_list:
            artists.append(Artist(
                name=a['name'],
                spotify_id=a['id']
            ))
        year, month, day = self._parse_album_release(
            album_obj['release_date'], 
            album_obj['release_date_precision'])
        album = Album(
            name=album_obj['name'],
            artists=artists_list,
            num_songs=album_obj['total_tracks'],
            spotify_id=album_obj['id'],
            release_year=year,
            release_month=month,
            release_day=day,
            spotify_album_type=album_obj['type']
        )
        return Song(
            name=json['name'],
            spotify_id=json['id'],
            duration_ms=json['duration_ms'],
            explicit=json['explicit'],
            album=album,
            artists=artists,
            song_number=json['disc_number'],
            spotify_is_local=json['is_local']
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
        res = self._session.get(
            url="{}tracks/?ids={}".format(self._base_url, ','.join(ids)),
            headers=self._gen_header(token)).json()
        
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
        res = self._session.get(
            url="{}me/tracks".format(self._base_url),
            headers=self._gen_header(token)).json()
        
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
                    headers=self._gen_header(token)).json()
            return ret_list

    def _add_saved_songs(self, songs: list[str], token: str) -> bool:
        """
        saves songs on spotify
        """
        res = self._session.put(
            url="{}me/tracks/?ids={}".format(self._base_url, ','.join(songs)),
            headers=self._gen_header(token))
        
        try:
            if 'error' in res.json():
                message = "Spotify API failed to save songs with ids " \
                + str(songs) + \
                " because of the following error: " + str(res['error'])
                raise RuntimeError(message)
        except JSONDecodeError:
            return True

    def _remove_saved_songs(self, songs: list[str], token: str) -> bool:
        """
        removes saved songs on spotify
        """
        res = self._session.delete(
            url="{}me/tracks/?ids={}".format(self._base_url, ','.join(songs)),
            headers=self._gen_header(token))
        
        try:
            if 'error' in res.json():
                message = "Spotify API failed to remove saved songs with ids " \
                + str(songs) + \
                " because of the following error: " + str(res['error'])
                raise RuntimeError(message)
        except JSONDecodeError:
            return True

    def _check_saved_songs(self, songs: list[str], token: str) -> bool:
        """
        checks saved songs on spotify
        """
        res = self._session.get(
            url="{}me/tracks/contains/?ids={}".format(self._base_url, 
            ','.join(songs)),
            headers=self._gen_header(token)).json()
        
        if 'error' in res:
            message = "Spotify API failed to remove saved songs with ids " \
            + str(songs) + \
            " because of the following error: " + str(res['error'])
            raise RuntimeError(message)
        else:
            return res
    
    def _search_song(self, song: Song, token: str) -> bool:
        """
        searchs for a song with avaialable info
        """
        if song.name is None:
            return song
        else:
            query_string = 'q=track:{}'.format(song.name, song.name)
            if song.artists is not None and len(song.artists) > 0 and \
            song.artists[0].name is not None:
                query_string += ' artist:{}'.format(song.artists[0].name)
            if song.album is not None and song.album.name is not None:
                query_string += ' album:{}'.format(song.album.name)
            
            query_string += '&type=track&limit=1'

            res = self._session.get(
            url="{}search?{}".format(self._base_url, query_string),
            headers=self._gen_header(token)).json()

            if 'error' in res:
                message = "Spotify API failed to populate song " \
                + song.name + \
                " because of the following error: " + str(res['error'])
                raise RuntimeError(message)
            else:
                if len(res['tracks']['items']) == 0:
                    return song
                else:
                    return self._create_song(res['tracks']['items'][0])
            
