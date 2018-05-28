import configparser
import logging

import requests

config = configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger(__name__)


class KKBOX:
    AUTH_URL = 'https://account.kkbox.com/oauth2/token'
    API_BASE_URL = 'https://api.kkbox.com/v1.1/'

    def __init__(self, id=config['KKBOX']['ID'], secret=config['KKBOX']['SECRET']):
        self.id = id
        self.secret = secret
        self.token = self._get_token()

    def _get_token(self):
        response = requests.post(self.AUTH_URL, data={'grant_type': 'client_credentials'}, auth=(self.id, self.secret))
        response.raise_for_status()
        return response.json()['access_token']

    def search(self, type, q, territory='TW'):
        response = requests.get(self.API_BASE_URL + 'search', params={'type': type, 'q': q, 'territory': territory},
                                headers={'Authorization': 'Bearer ' + self.token})
        response.raise_for_status()
        response_json = response.json()
        logger.error(response_json)
        result = {
            'artist': lambda: response_json['artists']['data'][0]['url'],
            'album': lambda: response_json['albums']['data'][0]['url'],
            'track': lambda: response_json['tracks']['data'][0]['url'],
            'playlist': lambda: response_json['playlists']['data'][0]['url']
        }[type]()
        return result
