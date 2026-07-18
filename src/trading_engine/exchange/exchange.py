from __future__ import annotations

from enum import Enum


class Exchange(str, Enum):

    OKX = "OKX"

    BINANCE = "BINANCE"

    BYBIT = "BYBIT"

    BITGET = "BITGET"