"""
Position enums.
"""

from enum import StrEnum


class PositionSide(StrEnum):
    """
    Position direction.
    """

    LONG = "long"
    SHORT = "short"
