# Python SDK for the OpenSea API

![python](https://github.com/FastestMolasses/PyOpenSea/actions/workflows/main.yaml/badge.svg)

An unofficial Python SDK for the [OpenSea API](https://docs.opensea.io/reference/api-overview).

## Features

-   Typing
-   All endpoints supported
-   Optional API key
-   WebSocket support

## Installation

```bash
pip install py-opensea
```

### Upgrade

```bash
pip install py-opensea -U
```

## Usage

```python
from pyopensea import OpenSeaAPI

# Create API instance
api = OpenSeaAPI('OPTIONAL-API-KEY')

# Examples
api.assets(owner='0x20481b79a4F03b624D214d23aDf5bF5f33bEB4aA')

api.contract('0x8a90cab2b38dba80c64b7734e58ee1db38b8992e')

api.listings('0x8a90cab2b38dba80c64b7734e58ee1db38b8992e', tokenID=10)

api.offers('0x8a90cab2b38dba80c64b7734e58ee1db38b8992e', tokenID=10, limit=5)

api.orders()

from datetime import datetime
api.orders('0x8a90cab2b38dba80c64b7734e58ee1db38b8992e',
           listedAfter=datetime(2022, 7, 5))

# And more api endpoints supported...
```

## Contributing

1. Fork it (<https://github.com/FastestMolasses/PyOpensea/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
