# QuantForge Engine

A modular quantitative trading framework.

## Development

Install the package with development tools:

```bash
python -m pip install -e ".[dev]"
```

Run validation:

```bash
python -m pytest
python -m ruff check .
python -m mypy src tests
```

## Example

```python
from datetime import UTC
from datetime import datetime
from decimal import Decimal

import ccxt

from quantforge.domain.value_objects import Candle
from quantforge.domain.value_objects import Price
from quantforge.domain.value_objects import Symbol
from quantforge.domain.value_objects import Timeframe
from quantforge.domain.value_objects import Volume
from quantforge.indicators import SimpleMovingAverage
from quantforge.providers import CcxtMarketDataProvider
from quantforge.strategy import MovingAverageCrossoverStrategy

candle = Candle(
    symbol=Symbol("BTC", "USDT"),
    timeframe=Timeframe("1h"),
    timestamp=datetime(2026, 7, 18, tzinfo=UTC),
    open_price=Price(Decimal("100")),
    high_price=Price(Decimal("120")),
    low_price=Price(Decimal("90")),
    close_price=Price(Decimal("110")),
    volume=Volume(Decimal("250")),
)

exchange = ccxt.binance()
provider = CcxtMarketDataProvider(client=exchange)
candles = provider.fetch_candles(
    symbol=Symbol("BTC", "USDT"),
    timeframe=Timeframe("1h"),
    limit=100,
)

sma = SimpleMovingAverage(period=20)
sma_values = sma.calculate(candles)

strategy = MovingAverageCrossoverStrategy(
    fast_period=20,
    slow_period=50,
)
signal = strategy.generate_signal(candles)
```
