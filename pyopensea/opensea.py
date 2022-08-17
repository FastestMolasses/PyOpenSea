import time
import requests

from datetime import datetime, timezone
from pyopensea.util import requireApiKey
from pyopensea.endpoint import Endpoints
from typing import Union, List, Literal, Generator

MAX_ASSETS = 50
MAX_ORDERS = 50
MAX_OFFERS = 50
MAX_OWNERS = 50
MAX_EVENTS = 300
MAX_BUNDLES = 50
MAX_LISTINGS = 50
MAX_COLLECTIONS = 300


class OpenSeaAPI:
    def __init__(self, apiKey: str = ''):
        self.apiKey = apiKey
        self.headers = {
            'Accept': 'application/json',
        }
        if apiKey:
            self.headers['X-API-KEY'] = apiKey

    @requireApiKey
    def assets(
        self,
        owner: str = None,
        tokenIDs: Union[List[Union[str, int]], str] = None,
        collectionSlug: str = None,
        collectionEditor: str = None,
        orderDirection: Literal['desc', 'asc'] = 'desc',
        contractAddress: str = None,
        contractAddresses: List[str] = None,
        includeOrders: bool = False,
        limit: int = MAX_ASSETS,
        cursor: str = None,
    ):
        params = {
            'owner': owner,
            'token_ids': tokenIDs,
            'collection_slug': collectionSlug,
            'collection_editor': collectionEditor,
            'order_direction': orderDirection,
            'asset_contract_address': contractAddress,
            'asset_contract_addresses': contractAddresses,
            'include_orders': 'true' if includeOrders else 'false',
            'limit': limit,
            'cursor': cursor,
        }
        return self._makeRequest(Endpoints.assets(), params)

    @requireApiKey
    def asset(
        self,
        contractAddress: str,
        tokenID: Union[str, int],
        accountAddress: str = None,
        includeOrders: bool = False,
    ):
        params = {
            'account_address': accountAddress,
            'include_orders': 'true' if includeOrders else 'false',
        }
        return self._makeRequest(Endpoints.asset(contractAddress, tokenID), params)

    @requireApiKey
    def contract(self, contractAddress: str):
        return self._makeRequest(Endpoints.contract(contractAddress))

    @requireApiKey
    def events(
        self,
        onlyOpensea: bool = False,
        tokenIDs: Union[List[Union[str, int]], str] = None,
        contractAddress: str = None,
        collectionSlug: str = None,
        collectionEditor: str = None,
        accountAddress: str = None,
        eventType: Literal['created', 'successful', 'cancelled', 'bid_entered',
                           'bid_withdrawn', 'transfer', 'offer_entered', 'approve'] = None,
        auctionType: Literal['english', 'dutch', 'min-price'] = None,
        occurredBefore: Union[datetime, int] = None,
        occurredAfter: Union[datetime, int] = None,
        cursor: str = None,
        limit: int = MAX_EVENTS,
    ):
        if isinstance(occurredBefore, datetime):
            occurredBefore = int(occurredBefore.replace(tzinfo=timezone.utc).timestamp())
        if isinstance(occurredAfter, datetime):
            occurredAfter = int(occurredAfter.replace(tzinfo=timezone.utc).timestamp())

        params = {
            'only_opensea': 'true' if onlyOpensea else 'false',
            'token_ids': tokenIDs,
            'asset_contract_address': contractAddress,
            'collection_slug': collectionSlug,
            'collection_editor': collectionEditor,
            'account_address': accountAddress,
            'event_type': eventType,
            'auction_type': auctionType,
            'occurred_before': occurredBefore,
            'occurred_after': occurredAfter,
            'cursor': cursor,
            'limit': limit,
        }
        return self._makeRequest(Endpoints.events(), params)

    @requireApiKey
    def eventsBackfill(
        self,
        onlyOpensea: bool = False,
        tokenIDs: Union[List[Union[str, int]], str] = None,
        contractAddress: str = None,
        collectionSlug: str = None,
        collectionEditor: str = None,
        accountAddress: str = None,
        eventType: Literal['created', 'successful', 'cancelled', 'bid_entered',
                           'bid_withdrawn', 'transfer', 'offer_entered', 'approve'] = None,
        auctionType: Literal['english', 'dutch', 'min-price'] = None,
        occurredBefore: Union[datetime, int] = None,
        occurredAfter: Union[datetime, int] = None,
        rateLimit: int = 2,
    ) -> Generator[List[dict], None, None]:
        """
            Backfill events from the OpenSea API. Starts at the specified recent event and
            continues until the specified time. Returns a generator that will
            yield the events in reverse chronological order.
        """
        cursor = None
        while True:
            time.sleep(rateLimit)
            result = self.events(
                onlyOpensea=onlyOpensea,
                tokenIDs=tokenIDs,
                contractAddress=contractAddress,
                collectionSlug=collectionSlug,
                collectionEditor=collectionEditor,
                accountAddress=accountAddress,
                eventType=eventType,
                auctionType=auctionType,
                occurredBefore=occurredBefore,
                occurredAfter=occurredAfter,
                cursor=cursor,
            )
            # Check if we have no results
            if result is None or len(result['asset_events']) == 0:
                break

            cursor = result['next']
            yield result['asset_events']

            # If there are no more results, end the loop
            if not result['next']:
                break

            # If occurredAfter is an int, convert it to a datetime object
            if isinstance(occurredAfter, int):
                occurredAfter = datetime.fromtimestamp(occurredAfter).replace(tzinfo=timezone.utc)

            # Get the last received date of event
            lastDate = datetime.strptime(
                result['asset_events'][-1]['created_date'],
                '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=timezone.utc)
            # Check if we've reached the end of the time range
            if lastDate < occurredAfter:
                break

    @requireApiKey
    def listings(
        self,
        contractAddress: str,
        tokenID: Union[str, int],
        limit: int = MAX_LISTINGS,
    ):
        params = {
            'limit': limit,
        }
        return self._makeRequest(Endpoints.listings(contractAddress, tokenID), params)

    @requireApiKey
    def offers(
        self,
        contractAddress: str,
        tokenID: Union[str, int],
        limit: int = MAX_OFFERS,
    ):
        params = {
            'limit': limit,
        }
        return self._makeRequest(Endpoints.offers(contractAddress, tokenID), params)

    @requireApiKey
    def orders(
        self,
        contractAddress: str = None,
        paymentTokenAddress: str = None,
        maker: str = None,
        taker: str = None,
        owner: str = None,
        isEnglish: bool = False,
        bundled: bool = False,
        includeBundled: bool = False,
        listedAfter: Union[datetime, int] = None,
        listedBefore: Union[datetime, int] = None,
        tokenID: Union[str, int] = None,
        tokenIDs: List[Union[str, int]] = None,
        side: Literal['buy', 'sell', 0, 1] = 1,
        saleKind: Literal[0, 1] = None,
        limit: int = MAX_ORDERS,
        offset: int = 0,
        orderBy: Literal['created_date', 'eth_price'] = 'created_date',
        orderDirection: Literal['desc', 'asc'] = 'desc',
    ):
        if isinstance(listedAfter, datetime):
            listedAfter = int(listedAfter.replace(tzinfo=timezone.utc).timestamp())
        if isinstance(listedBefore, datetime):
            listedBefore = int(listedBefore.replace(tzinfo=timezone.utc).timestamp())

        if side == 'buy':
            side = 0
        elif side == 'sell':
            side = 1

        params = {
            'asset_contract_address': contractAddress,
            'payment_token_address': paymentTokenAddress,
            'maker': maker,
            'taker': taker,
            'owner': owner,
            'is_english': 'true' if isEnglish else 'false',
            'bundled': 'true' if bundled else 'false',
            'include_bundled': 'true' if includeBundled else 'false',
            'listed_after': listedAfter,
            'listed_before': listedBefore,
            'token_id': tokenID,
            'token_ids': tokenIDs,
            'side': side,
            'sale_kind': saleKind,
            'limit': limit,
            'offset': offset,
            'order_by': orderBy,
            'order_direction': orderDirection,
        }
        return self._makeRequest(Endpoints.orders(), params)

    @requireApiKey
    def validateAsset(self, contractAddress: str, tokenID: Union[str, int]):
        return self._makeRequest(Endpoints.validateAsset(contractAddress, tokenID))

    def bundles(
        self,
        onSale: bool = False,
        owner: str = None,
        contractAddress: str = None,
        contractAddresses: List[str] = None,
        tokenIDs: List[Union[str, int]] = None,
        limit: int = MAX_BUNDLES,
        offset: int = 0,
    ):
        params = {
            'on_sale': 'true' if onSale else 'false',
            'owner': owner,
            'asset_contract_address': contractAddress,
            'asset_contract_addresses': contractAddresses,
            'token_ids': tokenIDs,
            'limit': limit,
            'offset': offset,
        }
        return self._makeRequest(Endpoints.bundles(), params)

    def collection(self, collectionSlug: str):
        return self._makeRequest(Endpoints.collection(collectionSlug))

    def collections(
        self,
        assetOwner: str = None,
        limit: int = MAX_COLLECTIONS,
        offset: int = 0,
    ):
        params = {
            'asset_owner': assetOwner,
            'limit': limit,
            'offset': offset,
        }
        return self._makeRequest(Endpoints.collections(), params)

    def collectionStats(self, collectionSlug: str):
        return self._makeRequest(Endpoints.collectionStats(collectionSlug))

    def owners(self,
               contractAddress: str,
               tokenID: Union[str, int],
               limit: int = MAX_OWNERS,
               orderBy: Literal['created_date'] = 'created_date',
               orderDirection: Literal['desc', 'asc'] = 'desc',
               cursor: str = None):
        params = {
            'limit': limit,
            'order_by': orderBy,
            'order_direction': orderDirection,
            'cursor': cursor,
        }
        return self._makeRequest(Endpoints.owners(contractAddress, tokenID), params)

    def _makeRequest(self, url: str, params: dict = None):
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 400:
            raise ValueError(response.text)

        elif response.status_code == 401:
            raise ValueError('Invalid API key')

        elif response.status_code == 403:
            raise ConnectionError('Access denied')

        elif response.status_code == 429:
            raise ConnectionError('Rate limit exceeded')

        elif response.status_code == 500:
            raise ConnectionError('Internal server error')

        return response.json()
