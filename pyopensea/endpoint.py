from typing import Union

BASE_URL = 'https://api.opensea.io/api/v1'


class Endpoints:
    def asset(contractAddress: str, tokenID: Union[str, int]) -> str:
        return f'{BASE_URL}/asset/{contractAddress}/{tokenID}'

    def assets() -> str:
        return f'{BASE_URL}/assets'

    def validateAsset(contractAddress: str, tokenID: Union[str, int]) -> str:
        return f'{BASE_URL}/asset/{contractAddress}/{tokenID}/validate'

    def events() -> str:
        return f'{BASE_URL}/events'

    def collection(collectionSlug: str) -> str:
        return f'{BASE_URL}/collection/{collectionSlug}'

    def collections() -> str:
        return f'{BASE_URL}/collections'

    def bundles() -> str:
        return f'{BASE_URL}/bundles'

    def contract(contractAddress: str) -> str:
        return f'{BASE_URL}/asset_contract/{contractAddress}'

    def collectionStats(collectionSlug: str) -> str:
        return f'{BASE_URL}/collection/{collectionSlug}/stats'

    def orders() -> str:
        return 'https://api.opensea.io/wyvern/v1/orders'

    def listings(contractAddress: str, tokenID: Union[str, int]) -> str:
        return f'{BASE_URL}/asset/{contractAddress}/{tokenID}/listings'

    def offers(contractAddress: str, tokenID: Union[str, int]) -> str:
        return f'{BASE_URL}/asset/{contractAddress}/{tokenID}/offers'
