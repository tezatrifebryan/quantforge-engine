"""
Volume value object.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from decimal import InvalidOperation

from quantforge.domain.exceptions import DomainValidationError


@dataclass(frozen=True, slots=True)
class Volume:
    """
    Immutable traded volume value object.
    """

    value: Decimal

    def __post_init__(self) -> None:
        """
        Validate and normalize value.
        """

        try:
            value = Decimal(self.value)
        except (InvalidOperation, TypeError) as exc:
            raise DomainValidationError("Volume must be a valid decimal.") from exc

        if value < 0:
            raise DomainValidationError("Volume cannot be negative.")

        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return str(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __add__(self, other: "Volume") -> "Volume":
        return Volume(self.value + other.value)

    def __sub__(self, other: "Volume") -> "Volume":
        return Volume(self.value - other.value)

    def __mul__(self, multiplier: Decimal | int | float) -> "Volume":
        return Volume(self.value * Decimal(str(multiplier)))

    def __truediv__(self, divisor: Decimal | int | float) -> "Volume":
        return Volume(self.value / Decimal(str(divisor)))

    def __lt__(self, other: "Volume") -> bool:
        return self.value < other.value

    def __le__(self, other: "Volume") -> bool:
        return self.value <= other.value

    def __gt__(self, other: "Volume") -> bool:
        return self.value > other.value

    def __ge__(self, other: "Volume") -> bool:
        return self.value >= other.value
