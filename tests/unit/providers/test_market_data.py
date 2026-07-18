from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from quantforge.domain.value_objects import Price, Symbol, Timeframe, Volume
from quantforge.providers import CcxtMarketDataProvider, ProviderError
from quantforge.providers.market_data import RawOhlcvRow


@dataclass(slots=True)
class FakeOhlcvClient:
    rows: Sequence[RawOhlcvRow]
    requested_symbol: str | None = None
    requested_timeframe: str | None = None
    requested_since: int | None = None
    requested_limit: int | None = None

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        since: int | None = None,
        limit: int | None = None,
    ) -> Sequence[RawOhlcvRow]:
        self.requested_symbol = symbol
        self.requested_timeframe = timeframe
        self.requested_since = since
        self.requested_limit = limit

        return self.rows


def test_fetch_candles_from_ohlcv_rows() -> None:
    client = FakeOhlcvClient(
        rows=(
            (
                1_784_332_800_000,
                "100",
                "120",
                "90",
                "110",
                "250",
            ),
        )
    )
    provider = CcxtMarketDataProvider(client)

    candles = provider.fetch_candles(
        symbol=Symbol("BTC", "USDT"),
        timeframe=Timeframe("1h"),
        since=datetime(2026, 7, 18, tzinfo=UTC),
        limit=100,
    )

    assert client.requested_symbol == "BTC/USDT"
    assert client.requested_timeframe == "1h"
    assert client.requested_since == 1_784_332_800_000
    assert client.requested_limit == 100
    assert len(candles) == 1
    assert candles[0].timestamp == datetime(2026, 7, 18, tzinfo=UTC)
    assert candles[0].open_price == Price(Decimal("100"))
    assert candles[0].high_price == Price(Decimal("120"))
    assert candles[0].low_price == Price(Decimal("90"))
    assert candles[0].close_price == Price(Decimal("110"))
    assert candles[0].volume == Volume(Decimal("250"))


def test_naive_since_datetime_is_treated_as_utc() -> None:
    client = FakeOhlcvClient(rows=())
    provider = CcxtMarketDataProvider(client)

    provider.fetch_candles(
        symbol=Symbol("BTC", "USDT"),
        timeframe=Timeframe("1h"),
        since=datetime(2026, 7, 18),
    )

    assert client.requested_since == 1_784_332_800_000


def test_fetch_limit_must_be_greater_than_zero() -> None:
    client = FakeOhlcvClient(rows=())
    provider = CcxtMarketDataProvider(client)

    with pytest.raises(ProviderError):
        provider.fetch_candles(
            symbol=Symbol("BTC", "USDT"),
            timeframe=Timeframe("1h"),
            limit=0,
        )


def test_ohlcv_row_must_contain_six_values() -> None:
    client = FakeOhlcvClient(
        rows=(
            (
                1_784_332_800_000,
                "100",
            ),
        )
    )
    provider = CcxtMarketDataProvider(client)

    with pytest.raises(ProviderError):
        provider.fetch_candles(
            symbol=Symbol("BTC", "USDT"),
            timeframe=Timeframe("1h"),
        )


def test_ohlcv_values_must_be_valid_decimals() -> None:
    client = FakeOhlcvClient(
        rows=(
            (
                1_784_332_800_000,
                "not-a-price",
                "120",
                "90",
                "110",
                "250",
            ),
        )
    )
    provider = CcxtMarketDataProvider(client)

    with pytest.raises(ProviderError):
        provider.fetch_candles(
            symbol=Symbol("BTC", "USDT"),
            timeframe=Timeframe("1h"),
        )
