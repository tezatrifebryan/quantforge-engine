"""
Order domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from quantforge.domain.enums import OrderSide
from quantforge.domain.enums import OrderStatus
from quantforge.domain.enums import OrderType
from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.value_objects import Price
from quantforge.domain.value_objects import Symbol
from quantforge.domain.value_objects import Volume


@dataclass(frozen=True, slots=True)
class Order:
    """
    Immutable order request.
    """

    order_id: str
    symbol: Symbol
    side: OrderSide
    order_type: OrderType
    quantity: Volume
    created_at: datetime
    price: Price | None = None
    status: OrderStatus = OrderStatus.PENDING

    def __post_init__(self) -> None:
        """
        Validate order consistency.
        """

        order_id = self.order_id.strip()

        if not order_id:
            raise DomainValidationError("Order id is required.")

        if self.quantity.value <= Decimal("0"):
            raise DomainValidationError("Order quantity must be greater than zero.")

        if self.order_type is OrderType.LIMIT and self.price is None:
            raise DomainValidationError("Limit order requires a price.")

        if self.order_type is OrderType.MARKET and self.price is not None:
            raise DomainValidationError("Market order cannot define a price.")

        object.__setattr__(self, "order_id", order_id)

    @property
    def is_buy(self) -> bool:
        """
        Return whether order side is buy.
        """

        return self.side is OrderSide.BUY

    @property
    def is_sell(self) -> bool:
        """
        Return whether order side is sell.
        """

        return self.side is OrderSide.SELL
