import requests

from pyopensea.endpoint import Endpoints
from pyopensea.util import requireApiKey


class OpenSeaAPI:
    def __init__(self, apiKey: str = ''):
        self.apiKey = apiKey
        self.headers = {
            'Accept': 'application/json',
        }
        if apiKey:
            self.headers['X-API-KEY'] = apiKey

    @requireApiKey
    def assets(self):
        return self._makeRequest(Endpoints.assets())

    def _makeRequest(self, url: str, params: dict = None):
        response = requests.get(url, headers=self.headers, params=params)

        # Make sure the API key is valid
        if response.status_code == 401:
            raise AttributeError('Invalid API key')

        return response.json()
