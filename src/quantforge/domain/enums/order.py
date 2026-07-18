"""
Order enums.
"""

from enum import StrEnum


class OrderSide(StrEnum):
    """
    Order direction.
    """

    BUY = "buy"
    SELL = "sell"


class OrderType(StrEnum):
    """
    Order execution type.
    """

    MARKET = "market"
    LIMIT = "limit"


class OrderStatus(StrEnum):
    """
    Order lifecycle status.
    """

    PENDING = "pending"
    OPEN = "open"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"
