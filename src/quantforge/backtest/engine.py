"""
Backtest engine.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from decimal import Decimal

from quantforge.backtest.exceptions import BacktestError
from quantforge.backtest.result import BacktestResult
from quantforge.domain.enums import OrderSide
from quantforge.domain.models import Order, Trade
from quantforge.domain.value_objects import Candle, Volume
from quantforge.execution import OrderExecutor
from quantforge.risk import SignalRiskManager
from quantforge.strategy import Signal, Strategy

MINIMUM_BACKTEST_CANDLES = 1
ZERO = Decimal("0")


@dataclass(frozen=True, slots=True)
class BacktestEngine:
    """
    Run a strategy over historical candles.
    """

    strategy: Strategy
    risk_manager: SignalRiskManager
    executor: OrderExecutor
    warmup_period: int

    def __post_init__(self) -> None:
        """
        Validate engine settings.
        """

        if self.warmup_period < MINIMUM_BACKTEST_CANDLES:
            raise BacktestError("Warmup period must be greater than zero.")

    def run(self, candles: Sequence[Candle]) -> BacktestResult:
        """
        Run backtest over candles.
        """

        if len(candles) < self.warmup_period:
            raise BacktestError("Not enough candles to run backtest.")

        signals: list[Signal] = []
        orders: list[Order] = []
        trades: list[Trade] = []
        open_quantity = ZERO

        for index in range(self.warmup_period, len(candles) + 1):
            candle_window = candles[:index]
            current_candle = candles[index - 1]
            signal = self.strategy.generate_signal(candle_window)
            order = self.risk_manager.create_order(signal)

            signals.append(signal)

            if order is None:
                continue

            adjusted_order = _adjust_long_only_order(
                order=order,
                open_quantity=open_quantity,
            )

            if adjusted_order is None:
                continue

            trade = self.executor.execute(
                order=adjusted_order,
                market_price=current_candle.close_price,
                executed_at=current_candle.timestamp,
            )
            open_quantity = _update_open_quantity(
                trade=trade,
                open_quantity=open_quantity,
            )

            orders.append(adjusted_order)
            trades.append(trade)

        return BacktestResult(
            signals=tuple(signals),
            orders=tuple(orders),
            trades=tuple(trades),
        )


def _adjust_long_only_order(
    order: Order,
    open_quantity: Decimal,
) -> Order | None:
    if order.side is OrderSide.BUY:
        return order

    if open_quantity == ZERO:
        return None

    if order.quantity.value <= open_quantity:
        return order

    return replace(
        order,
        quantity=Volume(open_quantity),
    )


def _update_open_quantity(
    trade: Trade,
    open_quantity: Decimal,
) -> Decimal:
    if trade.side is OrderSide.BUY:
        return open_quantity + trade.quantity.value

    return open_quantity - trade.quantity.value
