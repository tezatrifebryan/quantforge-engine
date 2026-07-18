"""
Trade domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from quantforge.domain.enums import OrderSide
from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.value_objects import Price
from quantforge.domain.value_objects import Symbol
from quantforge.domain.value_objects import Volume


@dataclass(frozen=True, slots=True)
class Trade:
    """
    Immutable executed trade.
    """

    trade_id: str
    order_id: str
    symbol: Symbol
    side: OrderSide
    price: Price
    quantity: Volume
    executed_at: datetime
    fee: Price = Price(Decimal("0"))

    def __post_init__(self) -> None:
        """
        Validate trade consistency.
        """

        trade_id = self.trade_id.strip()
        order_id = self.order_id.strip()

        if not trade_id:
            raise DomainValidationError("Trade id is required.")

        if not order_id:
            raise DomainValidationError("Order id is required.")

        if self.quantity.value <= Decimal("0"):
            raise DomainValidationError("Trade quantity must be greater than zero.")

        object.__setattr__(self, "trade_id", trade_id)
        object.__setattr__(self, "order_id", order_id)

    @property
    def notional(self) -> Price:
        """
        Return gross trade notional.
        """

        return self.price * self.quantity.value
