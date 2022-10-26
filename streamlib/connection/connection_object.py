from streamlib.cache import cache_handler
from ..cache import CacheHandler
from .spotify_auth_code import SpotifyAuthCode
from .spotify_api import SpotifyAPI


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

    def spotify_get_song_by_id(self, id: str):
        """
        This method takes a Spotify Song ID and creates a Song object for that 
        song. Song IDs can be found be getting a shareable link for a Spotify 
        song. Ex:
        https://open.spotify.com/track/xxx?si=yyy
        has the ID xxx

        params:

        id: the song id
        """
        return self._spotify_connection._get_song_by_id(
            id, 
            self._spotify_auth._access_token)
