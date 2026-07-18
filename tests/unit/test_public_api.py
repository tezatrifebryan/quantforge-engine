from quantforge import (
    BacktestEngine,
    Candle,
    CcxtMarketDataProvider,
    CsvBacktestWriter,
    ExponentialMovingAverage,
    FixedFractionPositionSizer,
    MovingAverageCrossoverStrategy,
    Order,
    PaperOrderExecutor,
    PerformanceReporter,
    Price,
    Signal,
    SignalRiskManager,
    SimpleMovingAverage,
    Symbol,
    Timeframe,
    Trade,
    Volume,
    __version__,
)


def test_public_api_exports_core_objects() -> None:
    assert __version__ == "0.1.0a1"
    assert BacktestEngine is not None
    assert Candle is not None
    assert CcxtMarketDataProvider is not None
    assert CsvBacktestWriter is not None
    assert ExponentialMovingAverage is not None
    assert FixedFractionPositionSizer is not None
    assert MovingAverageCrossoverStrategy is not None
    assert Order is not None
    assert PaperOrderExecutor is not None
    assert PerformanceReporter is not None
    assert Price is not None
    assert Signal is not None
    assert SignalRiskManager is not None
    assert SimpleMovingAverage is not None
    assert Symbol is not None
    assert Timeframe is not None
    assert Trade is not None
    assert Volume is not None
