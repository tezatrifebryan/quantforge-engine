"""
Paper order execution.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Protocol
from uuid import uuid4

from quantforge.domain.enums import OrderStatus, OrderType
from quantforge.domain.models import Order, Trade
from quantforge.domain.value_objects import Price
from quantforge.execution.exceptions import ExecutionError

ZERO = Decimal("0")
ONE = Decimal("1")
TRADE_ID_PREFIX = "trade"


class OrderExecutor(Protocol):
    """
    Contract for order execution.
    """

    def execute(
        self,
        order: Order,
        market_price: Price | None = None,
        executed_at: datetime | None = None,
    ) -> Trade:
        """
        Execute an order and return a trade.
        """


def _default_trade_id() -> str:
    return f"{TRADE_ID_PREFIX}-{uuid4()}"


@dataclass(frozen=True, slots=True)
class PaperOrderExecutor:
    """
    Simulated order executor.
    """

    fee_rate: Decimal = ZERO
    trade_id_factory: Callable[[], str] = _default_trade_id

    def __post_init__(self) -> None:
        """
        Validate executor settings.
        """

        if self.fee_rate < ZERO or self.fee_rate > ONE:
            raise ExecutionError("Fee rate must be between zero and one.")

    def execute(
        self,
        order: Order,
        market_price: Price | None = None,
        executed_at: datetime | None = None,
    ) -> Trade:
        """
        Execute an order immediately at simulated price.
        """

        if order.status is not OrderStatus.PENDING:
            raise ExecutionError("Only pending orders can be executed.")

        execution_price = _execution_price(
            order=order,
            market_price=market_price,
        )
        execution_time = executed_at or datetime.now(tz=UTC)
        fee = execution_price * order.quantity.value * self.fee_rate

        return Trade(
            trade_id=self.trade_id_factory(),
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side,
            price=execution_price,
            quantity=order.quantity,
            executed_at=execution_time,
            fee=fee,
        )


def _execution_price(order: Order, market_price: Price | None) -> Price:
    if market_price is not None:
        return market_price

    if order.order_type is OrderType.LIMIT and order.price is not None:
        return order.price

    raise ExecutionError("Market order requires execution price.")
