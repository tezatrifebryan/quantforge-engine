"""
Performance reporting.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal

from quantforge.domain.enums import OrderSide
from quantforge.domain.models import Trade
from quantforge.reporting.exceptions import ReportingError

ZERO = Decimal("0")
ONE_HUNDRED = Decimal("100")


@dataclass(frozen=True, slots=True)
class PerformanceSummary:
    """
    Immutable performance metrics summary.
    """

    trade_count: int
    closed_trade_count: int
    winning_trade_count: int
    open_quantity: Decimal
    average_entry_price: Decimal
    gross_pnl: Decimal
    total_fees: Decimal
    net_pnl: Decimal
    win_rate: Decimal


@dataclass(frozen=True, slots=True)
class PerformanceReporter:
    """
    Calculate long-only realized performance metrics from trades.
    """

    def summarize(self, trades: Sequence[Trade]) -> PerformanceSummary:
        """
        Summarize executed trades.
        """

        open_quantity = ZERO
        average_entry_price = ZERO
        gross_pnl = ZERO
        total_fees = ZERO
        closed_trade_count = 0
        winning_trade_count = 0

        for trade in trades:
            total_fees += trade.fee.value

            if trade.side is OrderSide.BUY:
                average_entry_price = _weighted_average_entry(
                    current_quantity=open_quantity,
                    current_average_entry=average_entry_price,
                    buy_quantity=trade.quantity.value,
                    buy_price=trade.price.value,
                )
                open_quantity += trade.quantity.value
                continue

            if trade.quantity.value > open_quantity:
                raise ReportingError("Sell trade quantity exceeds open quantity.")

            trade_pnl = (trade.price.value - average_entry_price) * trade.quantity.value
            gross_pnl += trade_pnl
            open_quantity -= trade.quantity.value
            closed_trade_count += 1

            if trade_pnl > ZERO:
                winning_trade_count += 1

            if open_quantity == ZERO:
                open_quantity = ZERO
                average_entry_price = ZERO

        return PerformanceSummary(
            trade_count=len(trades),
            closed_trade_count=closed_trade_count,
            winning_trade_count=winning_trade_count,
            open_quantity=open_quantity,
            average_entry_price=average_entry_price,
            gross_pnl=gross_pnl,
            total_fees=total_fees,
            net_pnl=gross_pnl - total_fees,
            win_rate=_win_rate(
                winning_trade_count=winning_trade_count,
                closed_trade_count=closed_trade_count,
            ),
        )


def _weighted_average_entry(
    current_quantity: Decimal,
    current_average_entry: Decimal,
    buy_quantity: Decimal,
    buy_price: Decimal,
) -> Decimal:
    total_quantity = current_quantity + buy_quantity

    if total_quantity == ZERO:
        return ZERO

    return (
        current_quantity * current_average_entry + buy_quantity * buy_price
    ) / total_quantity


def _win_rate(
    winning_trade_count: int,
    closed_trade_count: int,
) -> Decimal:
    if closed_trade_count == 0:
        return ZERO

    return Decimal(winning_trade_count) / Decimal(closed_trade_count) * ONE_HUNDRED
