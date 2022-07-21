import requests

from typing import Union
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

    @requireApiKey
    def asset(self, contractAddress: str, tokenID: Union[str, int]):
        return self._makeRequest(Endpoints.asset(contractAddress, tokenID))

    @requireApiKey
    def contract(self, contractAddress: str):
        return self._makeRequest(Endpoints.contract(contractAddress))

    @requireApiKey
    def listings(self, contractAddress: str, tokenID: Union[str, int]):
        return self._makeRequest(Endpoints.listings(contractAddress, tokenID))

    @requireApiKey
    def offers(self, contractAddress: str, tokenID: Union[str, int]):
        return self._makeRequest(Endpoints.offers(contractAddress, tokenID))

    @requireApiKey
    def orders(self):
        return self._makeRequest(Endpoints.orders())

    @requireApiKey
    def validateAsset(self, contractAddress: str, tokenID: Union[str, int]):
        return self._makeRequest(Endpoints.validateAsset(contractAddress, tokenID))

    def bundles(self):
        return self._makeRequest(Endpoints.bundles())

    def collection(self, collectionSlug: str):
        return self._makeRequest(Endpoints.collection(collectionSlug))

    def collections(self):
        return self._makeRequest(Endpoints.collections())

    def collectionStats(self, collectionSlug: str):
        return self._makeRequest(Endpoints.collectionStats(collectionSlug))

    def _makeRequest(self, url: str, params: dict = None):
        response = requests.get(url, headers=self.headers, params=params)

        # Make sure the API key is valid
        if response.status_code == 401:
            raise AttributeError('Invalid API key')

        elif response.status_code == 403:
            raise ConnectionError('Access denied')

        return response.json()
