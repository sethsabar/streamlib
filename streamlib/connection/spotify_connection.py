from streamlib.auth.spotify_authorization_code import SpotifyAuthorizationCode


class SpotifyConnection:

    def __init__(self):
        """
        The SpotifyConnection constructor.
        returns:
        A SpotifyConnection object.
        """
        self.auth_object = None

    def set_auth_code_connection(self, client_id, client_secret, redirect_uri):
        """
        Method which sets the SpotifyConnection's auth_object field to a
        SpotifyAuthorizationCode object. SpotifyAuthorizationCode objects use
        Spotify's Authorization Code Flow to access Spotify's API. Read more
        here: https://developer.spotify.com/documentation/general/guides/
        authorization/code-flow/. To set up a Spotify Developer App go here:
        https://developer.spotify.com/dashboard/applications
        params:
        client_id: string containing the client id of the Spotify Developer App
        client_secret: string containing the client secret of the Spotify
        Developer App
        redirect_uri: string containing the redirect uri of the Spotify
        Developer App
        """
        self.auth_object = SpotifyAuthorizationCode(client_id, client_secret,
                                                    redirect_uri)
