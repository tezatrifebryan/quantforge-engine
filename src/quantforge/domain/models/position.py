"""
Position domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from quantforge.domain.enums import PositionSide
from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.value_objects import Price, Symbol, Volume


@dataclass(frozen=True, slots=True)
class Position:
    """
    Immutable open position.
    """

    position_id: str
    symbol: Symbol
    side: PositionSide
    quantity: Volume
    entry_price: Price
    opened_at: datetime

    def __post_init__(self) -> None:
        """
        Validate position consistency.
        """

        position_id = self.position_id.strip()

        if not position_id:
            raise DomainValidationError("Position id is required.")

        if self.quantity.value <= Decimal("0"):
            raise DomainValidationError("Position quantity must be greater than zero.")

        object.__setattr__(self, "position_id", position_id)

    @property
    def notional(self) -> Price:
        """
        Return position entry notional.
        """

        return self.entry_price * self.quantity.value
