from __future__ import annotations

from enum import Enum


class TrendDirection(str, Enum):
    """
    Primary market trend direction.
    """

    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    SIDEWAYS = "SIDEWAYS"


class TrendStrength(str, Enum):
    """
    Trend strength classification.
    """

    VERY_WEAK = "VERY_WEAK"
    WEAK = "WEAK"
    NORMAL = "NORMAL"
    STRONG = "STRONG"
    VERY_STRONG = "VERY_STRONG"