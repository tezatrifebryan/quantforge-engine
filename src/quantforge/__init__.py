"""
QuantForge Engine

A modular quantitative trading framework.
"""

from .backtest import BacktestEngine, BacktestResult
from .domain import (
    Candle,
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    Position,
    PositionSide,
    Price,
    Symbol,
    Timeframe,
    Trade,
    Volume,
)
from .execution import PaperOrderExecutor
from .indicators import ExponentialMovingAverage, SimpleMovingAverage
from .providers import CcxtMarketDataProvider
from .reporting import PerformanceReporter, PerformanceSummary
from .risk import FixedFractionPositionSizer, SignalRiskManager
from .storage import CsvBacktestWriter
from .strategy import MovingAverageCrossoverStrategy, Signal, SignalAction
from .version import __version__

__all__ = [
    "BacktestEngine",
    "BacktestResult",
    "Candle",
    "CcxtMarketDataProvider",
    "CsvBacktestWriter",
    "ExponentialMovingAverage",
    "FixedFractionPositionSizer",
    "MovingAverageCrossoverStrategy",
    "Order",
    "OrderSide",
    "OrderStatus",
    "OrderType",
    "PaperOrderExecutor",
    "PerformanceReporter",
    "PerformanceSummary",
    "Position",
    "PositionSide",
    "Price",
    "Signal",
    "SignalAction",
    "SignalRiskManager",
    "SimpleMovingAverage",
    "Symbol",
    "Timeframe",
    "Trade",
    "Volume",
    "__version__",
]
