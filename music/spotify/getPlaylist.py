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

def main(playlist_id):
    headers = get_headers(client_id, client_secret)
    params = {
        "market" : "KR"
    }
    r = requests.get("https://api.spotify.com/v1/playlists/" + playlist_id, params=params, headers=headers)
    response_json = r.json()
    tracks = response_json['tracks']['items']
    
    track_names = []
    for item in tracks[:3]:
        track_name = item['track']['name']
        artists = [artist['name'] for artist in item['track']['artists']]  # 여러 아티스트가 있을 수 있으므로 리스트로 저장
        artist_names = ', '.join(artists)  # 아티스트 이름들을 쉼표로 구분하여 하나의 문자열로 결합
        track_names.append(f"{track_name} - {artist_names}")

    return track_names