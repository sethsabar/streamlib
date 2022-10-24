from ..cache import CacheHandler
from .spotify_auth_code_connection import SpotifyAuthCodeConnection

class ConnectionObject:
    def __init__(self, cache_folder=None, use_cache=True):
        if use_cache:
            if cache_folder is None:
                self.cache_handler = CacheHandler()
            else:
                self.cache_handler = CacheHandler(folder=cache_folder)
        else:
            self.cache_folder = None
        self.spotify_connnection = None
    
    def spotify_auth_code_connection(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: list[str] = None):
        if scope is None:
            self.spotify_connnection = SpotifyAuthCodeConnection(
                client_id, 
                client_secret, 
                redirect_uri,
                self.cache_handler)
        else:
            self.spotify_connnection = SpotifyAuthCodeConnection(
                client_id,
                client_secret, 
                redirect_uri, 
                self.cache_handler,
                scope)
