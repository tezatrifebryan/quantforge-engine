"""
Strategy contracts.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from quantforge.domain.value_objects import Candle
from quantforge.strategy.signal import Signal


class Strategy(Protocol):
    """
    Contract for candle-based strategies.
    """

    def generate_signal(self, candles: Sequence[Candle]) -> Signal:
        """
        Generate a trading signal from candles.
        """
