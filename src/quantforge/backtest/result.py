"""
Backtest result model.
"""

from __future__ import annotations

from dataclasses import dataclass

from quantforge.domain.models import Order, Trade
from quantforge.strategy import Signal


@dataclass(frozen=True, slots=True)
class BacktestResult:
    """
    Immutable backtest result.
    """

    signals: tuple[Signal, ...]
    orders: tuple[Order, ...]
    trades: tuple[Trade, ...]

    @property
    def signal_count(self) -> int:
        """
        Return generated signal count.
        """

        return len(self.signals)

    @property
    def order_count(self) -> int:
        """
        Return created order count.
        """

        return len(self.orders)

    @property
    def trade_count(self) -> int:
        """
        Return executed trade count.
        """

        return len(self.trades)
