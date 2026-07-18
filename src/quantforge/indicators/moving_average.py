"""
Moving average indicators.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from quantforge.domain.value_objects import Candle
from quantforge.domain.value_objects import Price
from quantforge.indicators.exceptions import IndicatorError

MINIMUM_PERIOD = 1
EMA_MULTIPLIER_NUMERATOR = Decimal("2")
EMA_MULTIPLIER_OFFSET = Decimal("1")


class Indicator(Protocol):
    """
    Contract for candle-based indicators.
    """

    def calculate(self, candles: Sequence[Candle]) -> tuple[Price, ...]:
        """
        Calculate indicator values from candles.
        """


@dataclass(frozen=True, slots=True)
class SimpleMovingAverage:
    """
    Simple moving average calculated from candle close prices.
    """

    period: int

    def __post_init__(self) -> None:
        """
        Validate period.
        """

        _validate_period(self.period)

    def calculate(self, candles: Sequence[Candle]) -> tuple[Price, ...]:
        """
        Calculate rolling simple moving average values.
        """

        _validate_candle_count(candles, self.period)

        close_values = tuple(candle.close_price.value for candle in candles)

        return tuple(
            Price(
                sum(
                    close_values[index : index + self.period],
                    Decimal("0"),
                )
                / Decimal(self.period)
            )
            for index in range(len(close_values) - self.period + 1)
        )


@dataclass(frozen=True, slots=True)
class ExponentialMovingAverage:
    """
    Exponential moving average calculated from candle close prices.
    """

    period: int

    def __post_init__(self) -> None:
        """
        Validate period.
        """

        _validate_period(self.period)

    def calculate(self, candles: Sequence[Candle]) -> tuple[Price, ...]:
        """
        Calculate exponential moving average values.
        """

        _validate_candle_count(candles, self.period)

        close_values = tuple(candle.close_price.value for candle in candles)
        multiplier = EMA_MULTIPLIER_NUMERATOR / (
            Decimal(self.period) + EMA_MULTIPLIER_OFFSET
        )
        values: list[Price] = []
        previous_value = close_values[0]

        values.append(Price(previous_value))

        for close_value in close_values[1:]:
            previous_value = close_value * multiplier + previous_value * (
                Decimal("1") - multiplier
            )
            values.append(Price(previous_value))

        return tuple(values)


def _validate_period(period: int) -> None:
    if period < MINIMUM_PERIOD:
        raise IndicatorError("Indicator period must be greater than zero.")


def _validate_candle_count(candles: Sequence[Candle], period: int) -> None:
    if len(candles) < period:
        raise IndicatorError("Not enough candles to calculate indicator.")
