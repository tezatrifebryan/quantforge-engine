from __future__ import annotations

from enum import Enum


class OrderSide(str, Enum):

    LONG = "LONG"

    SHORT = "SHORT"