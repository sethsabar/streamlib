from datetime import datetime, timedelta
import random
import string
from requests import Session
from urllib.parse import urlencode, urlparse, parse_qs
from base64 import b64encode
import warnings

class SpotifyAuthCodeConnection:

    # a list of all valid scopes the Spotify API allows. Read more here: 
    # https://developer.spotify.com/documentation/general/guides/authorization/scopes/
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
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._scope = self._parse_scopes(scope)
        self._session = Session()
        self._access_token = None
        self._refresh_token = None
        self._access_token_expires = None

    def _parse_scopes(self, scope: list[str]):
        return " ".join(scope)

    def _get_token(self, code):
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self._redirect_uri,
        }
        headers = {
            'Authorization': 'Basic %s' % b64encode('{}:{}'.format(self. \
            _client_id, self._client_secret).encode('ascii')).decode('ascii'),
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = self._session.post(
            url='https://accounts.spotify.com/api/token',
            params=payload,
            headers=headers
        ).json()
        if 'error' in response:
            error_message = \
                "Retrieving a token from the Spotify API failed with the " + \
                "following error: {}".format(response['error'])
            raise SpotifyAuthCodeException(error_message)
        else:
            new_scopes = self._parse_scopes(response['scope'])
            if not (set(new_scopes) == set(self._scope)):
                warnings.warn(
                    "Scopes allowed by Spotify don't match inputted scopes")
            else:
                self._access_token = response['access_token']
                self._refresh_token = response['refresh_token']
                self._access_token_expires = datetime.utcnow() + \
                timedelta(seconds=response['expires_in'])


    def _verify_credentials(self, uri: str, state: str):
        parsed_query = parse_qs(urlparse(uri).query)
        if 'error' in parsed_query:
            error_message = \
                "Spotify Authentication Failed with " + \
                "the following error: " + parsed_query['error'][0]
            raise SpotifyAuthCodeException(error_message)
        elif not (parsed_query['state'][0] == state):
            error_message = \
                "Returned state does not " + \
                "match sent state. Spotify account may be comprimised."
            raise SpotifyAuthCodeException(error_message)
        else:
            self._get_token(parsed_query['code'][0])



    def _prompt_user_login(self):
        state = ''.join(random.choices(string.ascii_letters, k=16))
        payload = {
            "client_id": self._client_id,
            "response_type": "code",
            "redirect_uri": self._redirect_uri,
            "state": state,
            "scope": self._scope,
        }
        auth_url = \
            'https://accounts.spotify.com/authorize?{}'. \
            format(urlencode(payload))
        print("Please copy this url into a web browser and allow your Spotify " 
        + "Application the requested permissions: {}".format(auth_url))
        self._verify_credentials(
            input("Then copy-paste the URI Spotify " +
                  "redirected you to and enter it here: "), state)


class SpotifyAuthCodeException(Exception):
    def __init__(self, message):
        super().__init__(message)