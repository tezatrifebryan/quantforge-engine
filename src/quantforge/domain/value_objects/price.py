"""
Price value object.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from decimal import InvalidOperation


from quantforge.domain.exceptions import DomainValidationError


@dataclass(frozen=True, slots=True)
class Price:
    """
    Immutable price value object.
    """

    value: Decimal

    def __post_init__(self) -> None:
        """
        Validate and normalize value.
        """

        try:
            value = Decimal(self.value)
        except (InvalidOperation, TypeError) as exc:
            raise DomainValidationError(
                "Price must be a valid decimal."
            ) from exc

        if value < 0:
            raise DomainValidationError(
                "Price cannot be negative."
            )

        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return str(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __add__(self, other: "Price") -> "Price":
        return Price(self.value + other.value)

    def __sub__(self, other: "Price") -> "Price":
        return Price(self.value - other.value)

    def __mul__(self, multiplier: Decimal | int | float) -> "Price":
        return Price(self.value * Decimal(str(multiplier)))

    def __truediv__(self, divisor: Decimal | int | float) -> "Price":
        return Price(self.value / Decimal(str(divisor)))

    def __lt__(self, other: "Price") -> bool:
        return self.value < other.value

    def __le__(self, other: "Price") -> bool:
        return self.value <= other.value

    def __gt__(self, other: "Price") -> bool:
        return self.value > other.value

    def __ge__(self, other: "Price") -> bool:
        return self.value >= other.value