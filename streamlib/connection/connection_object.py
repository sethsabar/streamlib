from typing import Any, Collection
from streamlib.cache.cache_handler import CacheHandler
from streamlib.connection.spotify_auth import SpotifyAuthCode
from streamlib.connection.spotify_api import SpotifyAPI
from streamlib.objects.song import Song
from streamlib.objects.artist import Artist
from streamlib.objects.album import Album


class ConnectionObject:

    def __init__(self, cache_folder: str = "streamlib_cache"):
        """
        Constructor for ConnectionObject object. This object wraps all 
        functionality of the streamlib library.

        params:

        (optional) cache_folder: the folder which will store the cache. The 
        default value is 'streamlib_cache'
        """
        self._cache_handler = CacheHandler(cache_folder)
        self._spotify_auth = None
        self._spotify_connection = SpotifyAPI()

    ## METHODS FOR INSTANTIATING API AUTHENTICATION ##
    
    def spotify_auth_code(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            scope: list[str] = None,
            check_cache: bool = True,
            update_cache: bool = True):
            """
            This method instantiates a SpotifyAuthCode object, which 
            authenticates Spotify API calls via the Authorization Code Flow. 
            Read more about this flow here: 
            https://developer.spotify.com/documentation/general/guides/authorization/code-flow/

            Go here to create a Spotify App:
            https://developer.spotify.com/dashboard/applications

            params:

            client_id: Spotify App client id
            client_secret: Spotify App client secret
            redirect_uri: Spoitfy App redirect uri
            (optional) scope: List of Spotify Authorization scopes, read more here: 
            https://developer.spotify.com/documentation/general/guides/authorization/scopes/
            (optional) check_cache: Whether this call should check the cache 
            for the API access token before prompting Spotify login and 
            verication of permissions
            (optional) update_cache: Whether this call should update the cache 
            with the credentials obtained from the Spotify API 
            """
            if scope is None:
                self._spotify_auth = SpotifyAuthCode(
                    client_id,
                    client_secret,
                    redirect_uri,
                    self._cache_handler,
                    check_cache=check_cache,
                    update_cache=update_cache)
            else:
                self._spotify_auth = SpotifyAuthCode(
                    client_id,
                    client_secret,
                    redirect_uri,
                    self._cache_handler,
                    scope,
                    check_cache,
                    update_cache)

    ## METHODS FOR CREATING OBJECTS FROM APIs ##

    def spotify_get_song_by_id(self, id: str):
        """
        This method takes a Spotify Song ID and creates a Song object for that 
        song. Song IDs can be found be getting a shareable link for a Spotify 
        song. Ex:
        https://open.spotify.com/track/xxx?si=yyy
        has the ID xxx

        params:

        id: the song id

        returns:

        a Song object
        """
        return self._spotify_connection._get_song_by_id(
            id, 
            self._spotify_auth._get_access_token())

    def spotify_get_songs_by_id(self, ids: list[str]):
        """
        This method takes a list of Spotify Song IDs and returns a list of Song 
        objects for those songs. Song IDs can be found be getting a shareable link for a Spotify 
        song. Ex:
        https://open.spotify.com/track/xxx?si=yyy
        has the ID xxx

        params:

        ids: the list of song ids

        returns:

        a list of Song objects
        """
        return self._spotify_connection._get_songs_by_id(
            ids, 
            self._spotify_auth._get_access_token())

    def spotify_get_saved_songs(self) -> list[Song]:
        """
        This method takes no parameters and returns a list of Song objects the 
        user has saved on Spotify
    
        returns:

        a list of Song objects the user has saved on Spotify
        """
        return self._spotify_connection._get_saved_songs(
            self._spotify_auth._get_access_token())
    
    def spotify_save_songs_by_id(self, songs: Collection[str]) -> bool:
        """
        This method takes a list of Spotify song IDs and adds them to the 
        logged in user's saved songs. On success True is returned
    
        params:

        songs: a collection of Spotify song ids

        returns:

        True if successful
        """
        return self._spotify_connection._add_saved_songs(
            list(songs),
            self._spotify_auth._get_access_token())

    ## METHODS FOR GETTING INFO ABOUT OBJECTS ##

    def get_song_info(
        self, 
        song: Song, 
        attr: Collection[str],
        with_inference: bool = True) -> dict[str, Any]:
        """
        This method takes in a Song object and a Collection of attributes and 
        returns a map from attribute name to attribute value. The valid 
        attributes are:

        name - get the name of the song
        artists - get a list of Artist objects who wrote the song
        album - get an Album object which the song is on
        spotify_id - get the Spotify ID for the song
        duration - get the duration of the song in milliseconds
        explicit - get a boolean indicating if the song is explicit

        params:

        song: a Song object
        attr: a list of attributes to retrieve
        (optional) with_inference: a bool indicating whether the method should 
        attempt to retrieve information not currently set in the object based 
        on the information that is currently available. True by default

        returns:

        a map from attribute name to attribute value for the Song object
        """
        return_map = {}
        to_get = set()
        if 'name' in attr:
            if song._name is None:
                to_get.add('name')
            else:
                return_map['name'] = song._name
        if 'artists' in attr:
            if song._artists is None:
                to_get.add('artists')
            else:
                return_map['artists'] = song._artists
        if 'album' in attr:
            if song._album is None:
                to_get.add('album')
            else:
                return_map['album'] = song._album
        if 'spotify_id' in attr:
            if song._album is None:
                to_get.add('spotify_id')
            else:
                return_map['spotify_id'] = song._spotify_id
        if 'duration' in attr:
            if song._album is None:
                to_get.add('duration')
            else:
                return_map['duration'] = song._duration
        if 'explicit' in attr:
            if song._album is None:
                to_get.add('explicit')
            else:
                return_map['explict'] = song._explicit
        
        if not with_inference:
            for item in to_get:
                return_map[item] = None
        elif (len(to_get) > 0) and (song._spotify_id is not None):
            copy: Song = self._spotify_connection._get_song_by_id(
                song._spotify_id, 
                self._spotify_auth._get_access_token())
            if 'name' in to_get:
                song._name = copy._name
                return_map['name'] = song._name
            if 'artists' in to_get:
                song._artists = copy._artists
                return_map['artists'] = song._artists
            if 'album' in to_get:
                song._album = copy._album
                return_map['album'] = song._album
            if 'spotify_id' in to_get:
                song._spotify_id = copy._spotify_id
                return_map['spotify_id'] = song._spotify_id
            if 'duration' in to_get:
                song._duration = copy._duration
                return_map['duration'] = song._duration
            if 'explicit' in to_get:
                song._explicit = copy._explicit
                return_map['explicit'] = song._explicit
        else:
            for item in to_get:
                return_map[item] = None
        
        return return_map

    
            

