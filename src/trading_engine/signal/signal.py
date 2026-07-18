from __future__ import annotations

from enum import Enum


class SignalType(str, Enum):
    """
    Trading signal.
    """

    BUY = "BUY"

    SELL = "SELL"

    HOLD = "HOLD"