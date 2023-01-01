import pytest

from pyopensea import OpenSeaAPI

# TODO: TEST API KEY ENDPOINTS

CRYPTO_PUNKS = '0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb'


@pytest.fixture
def api():
    return OpenSeaAPI('')


def test_bundles(api: OpenSeaAPI):
    bundles = api.bundles()
    assert bundles is not None


def test_collections(api: OpenSeaAPI):
    # Test singular collection
    collection = api.collection(CRYPTO_PUNKS)
    assert collection is not None

    # Test multiple collections
    collections = api.collections(CRYPTO_PUNKS, 1, 1)
    assert collections is not None


def test_collection_stats(api: OpenSeaAPI):
    collection_stats = api.collectionStats(CRYPTO_PUNKS)
    assert collection_stats is not None


def test_owners(api: OpenSeaAPI):
    owners = api.owners(CRYPTO_PUNKS, 1)
    assert owners is not None
