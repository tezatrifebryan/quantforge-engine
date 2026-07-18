from __future__ import annotations

from enum import Enum


class MarketStructure(str, Enum):

    UPTREND = "UPTREND"

    DOWNTREND = "DOWNTREND"

    RANGE = "RANGE"

    UNKNOWN = "UNKNOWN"