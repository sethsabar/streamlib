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

    ### SPOTIFY ###
    
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

    ## METHODS FOR COMMUNICATING WITH APIS ##

    ### SPOTIFY ###

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

    def spotify_removed_saved_songs_by_id(self, songs: Collection[str]) -> bool:
        """
        This method takes a list of Spotify song IDs and removes them from the 
        logged in user's saved songs. On success True is returned
    
        params:

        songs: a collection of Spotify song ids

        returns:

        True if successful
        """
        return self._spotify_connection._remove_saved_songs(
            list(songs),
            self._spotify_auth._get_access_token())
    
    def spotify_check_saved_songs_by_id(
        self, 
        songs: Collection[str]) -> list[bool]:
        """
        This method takes a list of Spotify song IDs and checks if they are saved. A list of booleans indicating if they are is returned
    
        params:

        songs: a collection of Spotify song ids

        returns:

        a list of booleans indicating if each song is saved
        """
        return self._spotify_connection._check_saved_songs(
            list(songs),
            self._spotify_auth._get_access_token())      

    def spotify_populate_song(self, song: Song) -> Song:
        """
        This method takes a Song object and returns a populated Song object 
        based on the currently available information in the object.
    
        params:

        song: a Song object

        returns:

        a Song object
        """
        if song.spotify_id is not None:
            return self.spotify_get_song_by_id(song.spotify_id)
        else:
            return self._spotify_connection._search_song(
            song,
            self._spotify_auth._get_access_token()) 

    ### APPLE MUSIC ###     
        
        
    
