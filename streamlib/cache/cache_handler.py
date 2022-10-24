from datetime import datetime
from os import mkdir
from os.path import isdir
import csv

class CacheHandler:

    def __init__(self, folder: str ="streamlib_cache"):
        if not isdir(folder):
            mkdir(folder)
        self.folder = folder

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
        file = open("{}/{}".format(self.folder, "sacc.csv"), 'a')
        writer = csv.writer(file)
        writer.writerow([
            client_id,
            client_secret,
            redirect_uri,
            scope,
            access_token,
            refresh_token,
            access_token_expires])
    
    def _spot_scope_parse(self, scope: str):
        return set(scope.split(" "))

    def _get_spotify_auth_code_connection(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: list[str],
        ):
        try:
            file = open("{}/{}".format(self.folder, "sacc.csv"), 'r')
            reader = csv.reader(file)
            for row in reader:
                if  (row[0] == client_id) and \
                    (row[1] == client_secret) and \
                    (row[2] == redirect_uri) and \
                    (self._spot_scope_parse(row[3]) == \
                    self._spot_scope_parse(scope)):  
                    return row[4], row[5], row[6]
            return None         
        except IOError:
            return None

        