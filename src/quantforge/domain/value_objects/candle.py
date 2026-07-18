"""
Candle value object.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.value_objects.price import Price
from quantforge.domain.value_objects.symbol import Symbol
from quantforge.domain.value_objects.timeframe import Timeframe
from quantforge.domain.value_objects.volume import Volume


@dataclass(frozen=True, slots=True)
class Candle:
    """
    Immutable OHLCV market candle.
    """

    symbol: Symbol
    timeframe: Timeframe
    timestamp: datetime
    open_price: Price
    high_price: Price
    low_price: Price
    close_price: Price
    volume: Volume

    def __post_init__(self) -> None:
        """
        Validate OHLC price consistency.
        """

        if self.high_price < self.low_price:
            raise DomainValidationError(
                "Candle high price cannot be lower than low price."
            )

        highest_trade_price = max(
            self.open_price,
            self.close_price,
        )

        if self.high_price < highest_trade_price:
            raise DomainValidationError(
                "Candle high price must include open and close prices."
            )

        lowest_trade_price = min(
            self.open_price,
            self.close_price,
        )

        if self.low_price > lowest_trade_price:
            raise DomainValidationError(
                "Candle low price must include open and close prices."
            )

    @property
    def is_bullish(self) -> bool:
        """
        Return whether close price is above open price.
        """

        return self.close_price > self.open_price

    @property
    def is_bearish(self) -> bool:
        """
        Return whether close price is below open price.
        """

        return self.close_price < self.open_price
