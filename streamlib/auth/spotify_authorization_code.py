import random
import string
from requests import Session
from urllib.parse import urlencode, urlparse, parse_qs
from webbrowser import open


class SpotifyAuthorizationCode:

    ALL_SCOPES = ["ugc-image-upload", "user-read-playback-state",
                  "user-modify-playback-state", "user-read-currently-playing",
                  "app-remote-control", "streaming", "playlist-read-private",
                  "playlist-read-collaborative", "playlist-modify-private",
                  "playlist-modify-public", "user-follow-modify",
                  "user-follow-read",
                  "user-read-playback-position", "user-top-read",
                  "user-read-recently-played", "user-library-modify",
                  "user-library-read", "user-read-email", "user-read-private"]

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            scope: list[str] = ALL_SCOPES):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.session = Session()
        self.scope = self._parse_scopes(scope)

    def _parse_scopes(self, scope: list[str]):
        return " ".join(scope)

    def _verify_and_cache_credentials(self, uri: str, state: str):
        parsed_query = parse_qs(urlparse(uri).query)
        if 'error' in parsed_query:
            error_message = \
                "Spotify Authentication Failed with " + \
                "the following error: " + parsed_query['error'][0]
            raise SpotifyAuthorizationCodeException(error_message)
        elif not (parsed_query['state'] == state):
            error_message = \
                "Returned state does not " + \
                "match sent state. Spotify account may be comprimised."
            raise SpotifyAuthorizationCodeException(error_message)

    def _prompt_user_login(self):
        state = ''.join(random.choices(string.ascii_letters, k=16))
        payload = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "state": state,
            "scope": self.scope,
        }
        auth_url = \
            'https://accounts.spotify.com/authorize?' + urlencode(payload)
        open(auth_url)
        self._verify_and_cache_credentials(
            input("Copy-paste the URI Spotify" +
                  "redirected you to and enter it here: "), state)


class SpotifyAuthorizationCodeException(Exception):
    def __init__(self, message):
        super().__init__(message)
