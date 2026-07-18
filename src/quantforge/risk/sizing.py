"""
Position sizing rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from quantforge.domain.value_objects import Price, Volume
from quantforge.risk.exceptions import RiskError

ZERO = Decimal("0")
ONE = Decimal("1")


class PositionSizer(Protocol):
    """
    Contract for position sizing rules.
    """

    def calculate_quantity(self, entry_price: Price) -> Volume:
        """
        Calculate order quantity for an entry price.
        """


@dataclass(frozen=True, slots=True)
class FixedFractionPositionSizer:
    """
    Size positions using a fixed account risk fraction.
    """

    account_equity: Price
    risk_fraction: Decimal
    stop_loss_fraction: Decimal

    def __post_init__(self) -> None:
        """
        Validate sizing parameters.
        """

        if self.account_equity.value <= ZERO:
            raise RiskError("Account equity must be greater than zero.")

        _validate_fraction(
            value=self.risk_fraction,
            field_name="Risk fraction",
        )
        _validate_fraction(
            value=self.stop_loss_fraction,
            field_name="Stop loss fraction",
        )

    def calculate_quantity(self, entry_price: Price) -> Volume:
        """
        Calculate position size from account risk and stop distance.
        """

        if entry_price.value <= ZERO:
            raise RiskError("Entry price must be greater than zero.")

        risk_amount = self.account_equity.value * self.risk_fraction
        risk_per_unit = entry_price.value * self.stop_loss_fraction

        return Volume(risk_amount / risk_per_unit)


def _validate_fraction(value: Decimal, field_name: str) -> None:
    if value <= ZERO or value > ONE:
        raise RiskError(f"{field_name} must be greater than zero and at most one.")
