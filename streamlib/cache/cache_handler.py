from os import mkdir
from os.path import isdir
import csv


class CacheHandler:

    def __init__(self, folder):
        """
        constructor for CacheHandler object, this should not be accessed directly
        """
        if not isdir(folder):
            mkdir(folder)
        self._folder = folder

    def _store_spotify_auth_code_connection(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: str,
        access_token: str,
        refresh_token: str,
        access_token_expires: str
        ):
        """
        given Spotify Auth Code Flow client info and credentials, stores them in the cache
        """
        file_w = open("{}/{}".format(self._folder, "sacc.csv"), 'w')
        file_r = open("{}/{}".format(self._folder, "sacc.csv"), 'r')
        reader = csv.reader(file_r)
        to_write = []
        already_in_cache = False
        for row in reader:
            if (row[0] == client_id) and \
                   (row[1] == client_secret) and \
                   (row[2] == redirect_uri) and \
                   (self._spot_scope_parse(row[3]) ==
                        self._spot_scope_parse(scope)):
                already_in_cache = True
                to_write.append(
                    [client_id,
                    client_secret,
                    redirect_uri,
                    scope,
                    access_token,
                    refresh_token,
                    access_token_expires])
            else:
                to_write.append(row)
        if not already_in_cache:
            to_write.append(
                    [client_id,
                    client_secret,
                    redirect_uri,
                    scope,
                    access_token,
                    refresh_token,
                    access_token_expires])
        writer = csv.writer(file_w)
        writer.writerows(to_write)

    def _spot_scope_parse(self, scope: str):
        """
        Parses a string of Spotify scopes into a set of scopes
        """
        return set(scope.split(" "))

    def _get_spotify_auth_code_connection(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: list[str],
            ):
        """
        given Spotify Auth Code Flow client info, looks for credentials in the 
        cache
        """
        try:
            file = open("{}/{}".format(self._folder, "sacc.csv"), 'r')
            reader = csv.reader(file)
            for row in reader:
                if (row[0] == client_id) and \
                   (row[1] == client_secret) and \
                   (row[2] == redirect_uri) and \
                   (self._spot_scope_parse(row[3]) ==
                        self._spot_scope_parse(scope)):
                    return row[4], row[5], row[6]
            return None
        except IOError:
            return None
