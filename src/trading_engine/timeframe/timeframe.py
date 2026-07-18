from __future__ import annotations

from enum import Enum


class Timeframe(str, Enum):

    M1 = "1m"

    M3 = "3m"

    M5 = "5m"

    M15 = "15m"

    M30 = "30m"

    H1 = "1H"

    H4 = "4H"

    D1 = "1D"

    W1 = "1W"