"""
QuantForge strategy layer.
"""

from .exceptions import StrategyError
from .moving_average import MovingAverageCrossoverStrategy
from .signal import Signal, SignalAction
from .strategy import Strategy

__all__ = [
    "MovingAverageCrossoverStrategy",
    "Signal",
    "SignalAction",
    "Strategy",
    "StrategyError",
]
