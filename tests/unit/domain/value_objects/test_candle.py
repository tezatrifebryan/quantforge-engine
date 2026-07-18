from datetime import UTC
from datetime import datetime
from decimal import Decimal

import pytest

from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.value_objects import Candle
from quantforge.domain.value_objects import Price
from quantforge.domain.value_objects import Symbol
from quantforge.domain.value_objects import Timeframe
from quantforge.domain.value_objects import Volume


def test_create_bullish_candle() -> None:
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

    assert candle.is_bullish
    assert not candle.is_bearish


def test_create_bearish_candle() -> None:
    candle = Candle(
        symbol=Symbol("BTC", "USDT"),
        timeframe=Timeframe("1h"),
        timestamp=datetime(2026, 7, 18, tzinfo=UTC),
        open_price=Price(Decimal("110")),
        high_price=Price(Decimal("120")),
        low_price=Price(Decimal("90")),
        close_price=Price(Decimal("100")),
        volume=Volume(Decimal("250")),
    )

    assert candle.is_bearish
    assert not candle.is_bullish


def test_high_price_cannot_be_lower_than_low_price() -> None:
    with pytest.raises(DomainValidationError):
        Candle(
            symbol=Symbol("BTC", "USDT"),
            timeframe=Timeframe("1h"),
            timestamp=datetime(2026, 7, 18, tzinfo=UTC),
            open_price=Price(Decimal("100")),
            high_price=Price(Decimal("80")),
            low_price=Price(Decimal("90")),
            close_price=Price(Decimal("95")),
            volume=Volume(Decimal("250")),
        )


def test_high_price_must_include_open_and_close_prices() -> None:
    with pytest.raises(DomainValidationError):
        Candle(
            symbol=Symbol("BTC", "USDT"),
            timeframe=Timeframe("1h"),
            timestamp=datetime(2026, 7, 18, tzinfo=UTC),
            open_price=Price(Decimal("100")),
            high_price=Price(Decimal("105")),
            low_price=Price(Decimal("90")),
            close_price=Price(Decimal("110")),
            volume=Volume(Decimal("250")),
        )


def test_low_price_must_include_open_and_close_prices() -> None:
    with pytest.raises(DomainValidationError):
        Candle(
            symbol=Symbol("BTC", "USDT"),
            timeframe=Timeframe("1h"),
            timestamp=datetime(2026, 7, 18, tzinfo=UTC),
            open_price=Price(Decimal("100")),
            high_price=Price(Decimal("120")),
            low_price=Price(Decimal("105")),
            close_price=Price(Decimal("110")),
            volume=Volume(Decimal("250")),
        )
