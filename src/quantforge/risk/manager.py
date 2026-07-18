"""
Signal risk manager.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from uuid import uuid4

from quantforge.domain.enums import OrderSide, OrderType
from quantforge.domain.models import Order
from quantforge.risk.sizing import PositionSizer
from quantforge.strategy import Signal, SignalAction

ORDER_ID_PREFIX = "order"


def _default_order_id() -> str:
    return f"{ORDER_ID_PREFIX}-{uuid4()}"


@dataclass(frozen=True, slots=True)
class SignalRiskManager:
    """
    Convert approved strategy signals into orders.
    """

    position_sizer: PositionSizer
    order_id_factory: Callable[[], str] = _default_order_id

    def create_order(self, signal: Signal) -> Order | None:
        """
        Create an order from a signal when risk rules approve it.
        """

        if signal.action is SignalAction.HOLD:
            return None

        return Order(
            order_id=self.order_id_factory(),
            symbol=signal.symbol,
            side=_order_side(signal.action),
            order_type=OrderType.MARKET,
            quantity=self.position_sizer.calculate_quantity(signal.price),
            created_at=signal.generated_at,
        )


def _order_side(action: SignalAction) -> OrderSide:
    if action is SignalAction.BUY:
        return OrderSide.BUY

    return OrderSide.SELL
