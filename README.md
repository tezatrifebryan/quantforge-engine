# QuantForge Engine

A modular quantitative trading framework for research, backtesting, and paper execution.

QuantForge is currently an alpha engine. The core path is intentionally small and typed:

```text
provider -> Candle -> indicator -> strategy Signal -> risk Order -> execution Trade -> backtest result -> performance summary
```

## Features

- Immutable domain objects for market data, orders, trades, and positions.
- CCXT-compatible market data provider that normalizes OHLCV rows into `Candle`.
- SMA and EMA indicators.
- Moving average crossover strategy.
- Fixed-fraction risk sizing and signal-to-order conversion.
- Paper order execution with fee simulation.
- Minimal backtest engine.
- Performance reporting for realized long-only PnL.

## Install

```bash
python -m pip install -e ".[dev]"
```

## Validate

```bash
python -m pytest
python -m coverage run -m pytest
python -m coverage report
python -m ruff check .
python -m ruff format --check .
python -m mypy src tests scripts
```

## Quickstart

```python
from datetime import UTC
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import ccxt

from quantforge import BacktestEngine
from quantforge import Candle
from quantforge import CcxtMarketDataProvider
from quantforge import CsvBacktestWriter
from quantforge import FixedFractionPositionSizer
from quantforge import MovingAverageCrossoverStrategy
from quantforge import PaperOrderExecutor
from quantforge import PerformanceReporter
from quantforge import Price
from quantforge import SignalRiskManager
from quantforge import SimpleMovingAverage
from quantforge import Symbol
from quantforge import Timeframe
from quantforge import Volume

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

sizer = FixedFractionPositionSizer(
    account_equity=Price(Decimal("1000")),
    risk_fraction=Decimal("0.02"),
    stop_loss_fraction=Decimal("0.05"),
)
risk_manager = SignalRiskManager(position_sizer=sizer)
order = risk_manager.create_order(signal)

if order is not None:
    executor = PaperOrderExecutor(fee_rate=Decimal("0.001"))
    trade = executor.execute(
        order=order,
        market_price=signal.price,
    )

backtest = BacktestEngine(
    strategy=strategy,
    risk_manager=risk_manager,
    executor=PaperOrderExecutor(fee_rate=Decimal("0.001")),
    warmup_period=50,
)
result = backtest.run(candles)

reporter = PerformanceReporter()
summary = reporter.summarize(result.trades)

CsvBacktestWriter(output_dir=Path("data/backtests/demo")).write(
    result=result,
    summary=summary,
)
```

## Offline Demo

Run the local demo without exchange/network access:

```bash
python scripts/offline_backtest.py
```

It writes `summary.csv` and `trades.csv` under `data/backtests/offline_demo`.

## Project Status

QuantForge is usable for deterministic unit-tested research flows, but it is not production live-trading software yet. Live execution, portfolio accounting, short-selling metrics, and richer exchange error handling are future milestones.
