from dotenv import load_dotenv
import os

import sys
import requests
import base64
import json
import logging


load_dotenv()

client_id = os.getenv('SPOTIFY_ID')
client_secret = os.getenv('SPOTIFY_SECRET')

def get_headers(cliend_id, client_secret):
    endpoint = "https://accounts.spotify.com/api/token"
    encoded = base64.b64encode("{}:{}".format(client_id, client_secret).encode('utf-8')).decode('ascii')
    headers = {
        "Authorization": "Basic {}".format(encoded)
    }
    payload = {
        "grant_type": "client_credentials"
    }
    r = requests.post(endpoint, data=payload, headers=headers)
    access_token = json.loads(r.text)['access_token']
    headers = {
        "Authorization": "Bearer {}".format(access_token)
    }
    return headers

def main(emotion, keyword):
    headers = get_headers(client_id, client_secret)
    params = {
        "q" : emotion + "%" + keyword,
        "type" : "playlist",
        "limit" : "1",
        "market" : "KR",
        "offset" : "5"
    }

    r = requests.get("https://api.spotify.com/v1/search", params=params, headers=headers)
    response_json = r.json()
    playlist_id = response_json['playlists']['items'][0]['id']

    return playlist_id