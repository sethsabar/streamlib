from datetime import datetime, timedelta
import random
import string
from requests import Session
from urllib.parse import urlencode, urlparse, parse_qs
from base64 import b64encode
import warnings
from ..cache import CacheHandler


class SpotifyAuthCode:

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

    BASE_URL = "https://accounts.spotify.com/api/token"

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            cache_handler: CacheHandler,
            scope: list[str] = ALL_SCOPES,
            check_cache: bool = True,
            update_cache: bool = True):
            """
            constructor for SpotifyAuthCode object, this should not be accessed 
            directly
            """
            self._client_id: str = client_id
            self._client_secret: str = client_secret
            self._redirect_uri: str = redirect_uri
            self._cache_handler: CacheHandler = cache_handler
            self._scope: str = self._parse_scopes(scope)
            self._session: Session = Session()
            self._access_token: str = None
            self._refresh_token: str = None
            self._access_token_expires: datetime = None
            self._update_cache: bool = update_cache
            if (not check_cache) or (not self._check_cache()):
                self._prompt_user_login()

    def _check_cache(self) -> bool:
        """
        checks with the CacheHandler if the credentials associated with the 
        client info already exist in the cache
        """
        result = self._cache_handler._get_spotify_auth_code_connection(
            self._client_id,
            self._client_secret,
            self._redirect_uri,
            self._scope)
        if result is not None:
            self._access_token = result[0]
            self._refresh_token = result[1]
            self._access_token_expires = datetime.strptime(result[2]
            , '%Y-%m-%d %H:%M:%S.%f')
            return True
        else:
            return False

    def _parse_scopes(self, scope: list[str]) -> str:
        """
        parses the list of scopes into a space seperated string of scopes
        """
        return " ".join(scope)

    def _get_token(self, code: str) -> None:
        """
        gets the access token for Spotify API calls
        """
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self._redirect_uri,
        }

        headers = {
            'Authorization': 'Basic %s' %
            b64encode('{}:{}'.format(self._client_id,
                                     self._client_secret).
                      encode('ascii')).decode('ascii'),
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = self._session.post(
            url=self.BASE_URL,
            params=payload,
            headers=headers
        ).json()
        self._get_access_token_helper(headers, response)  

    def _verify_credentials(self, uri: str, state: str) -> None:
        """
        takes the uri Spotify redirected the user to after verifying permissions
        and the state given in the Spotify call and verifies that the uri is
        legit, and uses the given code to get an access token
        """
        parsed_query = parse_qs(urlparse(uri).query)
        if 'error' in parsed_query:
            error_message = \
                "Spotify Authentication Failed with " + \
                "the following error: " + parsed_query['error'][0]
            raise RuntimeError(error_message)
        elif not (parsed_query['state'][0] == state):
            error_message = \
                "Returned state does not " + \
                "match sent state. Spotify account may be comprimised."
            raise RuntimeError(error_message)
        else:
            self._get_token(parsed_query['code'][0])

    
    def _prompt_user_login(self) -> None:
        """
        prompts the user to login and verify the API permissions
        """
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

    def _get_access_token_helper(self, payload, headers) -> None:
        """
        helper method which takes a payload and headers to get an access token,
        and parses the response to set fields in the object
        """
        response = self._session.post(
                url=self.BASE_URL, 
                params=payload,
                headers=headers).json()
        if 'error' in response:
            error_message = \
            "Retrieving a token from the Spotify API failed with the " + \
            "following error: {}".format(response['error'])
            raise RuntimeError(error_message)
        else:
            new_scopes = self._parse_scopes(response['scope'])
            if not (set(new_scopes) == set(self._scope)):
                warnings.warn(
                    "Scopes allowed by Spotify don't match inputted scopes")
                self._scope = new_scopes
            else:
                self._access_token = response['access_token']
                if 'refresh_token' in response:
                    self._refresh_token = response['refresh_token']
                self._access_token_expires = datetime.utcnow() + \
                    timedelta(seconds=response['expires_in'])
        if self._update_cache:
            self._cache_handler._store_spotify_auth_code_connection(
                self._client_id,
                self._client_secret,
                self._redirect_uri,
                self._scope,
                self._access_token,
                self._refresh_token,
                self._access_token_expires
            )

    def _get_access_token(self) -> str:
        """
        gets the access token if it hasn't yet expried, otherwise uses the 
        refresh token to get a new access token
        """
        if self._access_token_expires < datetime.utcnow():
            payload = {
                'grant_type':'refresh_token',
                'refresh_token': self._refresh_token,
            }
            headers = {
            'Authorization': 'Basic %s' %
            b64encode('{}:{}'.format(self._client_id,
                                     self._client_secret).
                      encode('ascii')).decode('ascii'),
            'Content-Type': 'application/x-www-form-urlencoded',
            }
            self._get_access_token_helper(payload, headers)
        return self._access_token
