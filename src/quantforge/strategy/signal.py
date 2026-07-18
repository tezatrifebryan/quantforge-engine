"""
Strategy signal domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from quantforge.domain.value_objects import Price, Symbol


class SignalAction(StrEnum):
    """
    Trading signal action.
    """

    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


@dataclass(frozen=True, slots=True)
class Signal:
    """
    Immutable strategy signal.
    """

    symbol: Symbol
    action: SignalAction
    price: Price
    generated_at: datetime
    reason: str
