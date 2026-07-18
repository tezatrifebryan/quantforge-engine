"""
Timeframe value object.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import ClassVar

from quantforge.domain.exceptions import DomainValidationError


@dataclass(frozen=True, slots=True)
class Timeframe:
    """
    Immutable market data timeframe.
    """

    DURATIONS: ClassVar[dict[str, timedelta]] = {
        "1m": timedelta(minutes=1),
        "3m": timedelta(minutes=3),
        "5m": timedelta(minutes=5),
        "15m": timedelta(minutes=15),
        "30m": timedelta(minutes=30),
        "1h": timedelta(hours=1),
        "4h": timedelta(hours=4),
        "1d": timedelta(days=1),
        "1w": timedelta(weeks=1),
    }

    value: str

    def __post_init__(self) -> None:
        """
        Validate and normalize value.
        """

        value = self.value.strip().lower()

        if value not in self.DURATIONS:
            raise DomainValidationError("Timeframe is not supported.")

        object.__setattr__(self, "value", value)

    @property
    def duration(self) -> timedelta:
        """
        Return timeframe duration.
        """

        return self.DURATIONS[self.value]

    def __str__(self) -> str:
        return self.value
