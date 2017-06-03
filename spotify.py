import requests
import base64
import os
from pprint import pprint
os.chdir('..')
print(os.getcwd())


class Connection:
    """
    Class' object instantiates a connection with spotify. When the connection is alive, queries are made with the query_get
    method.
    """

    def __init__(self, client_id=None, secret=None):
        if client_id is None:
            client_id = open("./ignore/id.txt").read()
        if secret is None:
            secret = open("./ignore/secret.txt").read()
        # First header and parameters needed to require an access token.
        param = {"grant_type": "client_credentials"}
        header = {"Authorization": "Basic {}".format(
            base64.b64encode("{}:{}".format(client_id, secret).encode("ascii")).decode("ascii")),
            'Content-Type': 'application/x-www-form-urlencoded'}
        self.token = requests.post("https://accounts.spotify.com/api/token", param, headers=header).json()[
            "access_token"]
        self.header = {"Authorization": "Bearer {}".format(self.token)}
        self.base_url = "https://api.spotify.com"

    def query_get(self, query, params=None):
        """

        :param query: (str) URL coming after example.com
        :param params: (dict)
        :return: (json) 
        """
        return requests.get(self.base_url + query, params, headers=self.header).json()

    def query_track(self, track):
        """
        Query a track name.
        
        :param track: (str)
        :return: (dict)
        """
        return self.query_get("/v1/search/",
                            {'q': "{}".format(track.replace(' ', '+')), "type": ("track", "artist")})

    def track_preview(self, track, index=0):
        """
        Get a preview url of a track query.
        :param track: (str)
        :return: (str)
        """
        return self.query_track(track)["tracks"]["items"][index]["preview_url"]

    def artist_track_preview(self, artist, track):
        """
        Get a preview url of a track query
        :param artist: (str)
        :param track: (str)
        :return: (str)
        """
        artist = artist.lower()
        q = self.query_track("{} - {}".format(artist, track))["tracks"]["items"]
        for d in q:
            if d["artists"][0]["name"].lower() == artist and d["preview_url"]:
                return d["preview_url"]

        # try again for partial match
        for d in q:
            if artist in d["artists"][0]["name"].lower() and d["preview_url"]:
                return d["preview_url"]


