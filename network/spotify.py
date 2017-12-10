#!/usr/bin/env python3

"""
Beispielskript zum Zugriff auf die Spotify API.

Anmeldung einer App für die Client-ID und das Client-Secret: https://beta.developer.spotify.com/dashboard/
Informationen zur Authentifizierung: https://developer.spotify.com/web-api/authorization-guide/#client-credentials-flow

"""

import json
import base64
from urllib.parse import quote

import requests


def get_token():
    url = 'https://accounts.spotify.com/api/token'
    client_id_and_secret = '{client_id}:{client_secret}'.format(client_id='', client_secret='')
    client_data = base64.urlsafe_b64encode(client_id_and_secret.encode()).decode()
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': 'Basic {}'.format(client_data)}
    payload = {'grant_type': 'client_credentials'}
    r = requests.post(url, headers=headers, data=payload)
    server_data = json.loads(r.text)
    return server_data['access_token']


def search_artists(artist):
    url = 'https://api.spotify.com/v1/search?type=artist&q={}'.format(quote(artist))
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': 'Bearer {}'.format(token)}
    r = requests.get(url, headers=headers)
    return r.text


token = get_token()
print('Token: {}'.format(token))
artist_info = search_artists('Die Ärzte')
print(artist_info)
