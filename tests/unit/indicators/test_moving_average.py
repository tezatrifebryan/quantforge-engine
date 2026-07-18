from datetime import UTC
from datetime import datetime
from decimal import Decimal

import pytest

from quantforge.domain.value_objects import Candle
from quantforge.domain.value_objects import Price
from quantforge.domain.value_objects import Symbol
from quantforge.domain.value_objects import Timeframe
from quantforge.domain.value_objects import Volume
from quantforge.indicators import ExponentialMovingAverage
from quantforge.indicators import IndicatorError
from quantforge.indicators import SimpleMovingAverage


def test_simple_moving_average() -> None:
    indicator = SimpleMovingAverage(period=3)

    values = indicator.calculate(
        _candles(
            close_values=(
                Decimal("10"),
                Decimal("20"),
                Decimal("30"),
                Decimal("40"),
            )
        )
    )

    assert values == (
        Price(Decimal("20")),
        Price(Decimal("30")),
    )


def test_exponential_moving_average() -> None:
    indicator = ExponentialMovingAverage(period=3)

    values = indicator.calculate(
        _candles(
            close_values=(
                Decimal("10"),
                Decimal("20"),
                Decimal("30"),
            )
        )
    )

    assert values == (
        Price(Decimal("10")),
        Price(Decimal("15.0")),
        Price(Decimal("22.50")),
    )


def test_indicator_period_must_be_greater_than_zero() -> None:
    with pytest.raises(IndicatorError):
        SimpleMovingAverage(period=0)


def test_simple_moving_average_requires_enough_candles() -> None:
    indicator = SimpleMovingAverage(period=3)

    with pytest.raises(IndicatorError):
        indicator.calculate(
            _candles(
                close_values=(
                    Decimal("10"),
                    Decimal("20"),
                )
            )
        )


def test_exponential_moving_average_requires_enough_candles() -> None:
    indicator = ExponentialMovingAverage(period=3)

    with pytest.raises(IndicatorError):
        indicator.calculate(
            _candles(
                close_values=(
                    Decimal("10"),
                    Decimal("20"),
                )
            )
        )


def _candles(close_values: tuple[Decimal, ...]) -> tuple[Candle, ...]:
    return tuple(
        Candle(
            symbol=Symbol("BTC", "USDT"),
            timeframe=Timeframe("1h"),
            timestamp=datetime(2026, 7, 18, index, tzinfo=UTC),
            open_price=Price(close_value),
            high_price=Price(close_value),
            low_price=Price(close_value),
            close_price=Price(close_value),
            volume=Volume(Decimal("1")),
        )
        for index, close_value in enumerate(close_values)
    )
