"""
Run an offline QuantForge backtest and write CSV output.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from quantforge import (
    BacktestEngine,
    Candle,
    CsvBacktestWriter,
    FixedFractionPositionSizer,
    MovingAverageCrossoverStrategy,
    PaperOrderExecutor,
    PerformanceReporter,
    Price,
    SignalRiskManager,
    Symbol,
    Timeframe,
    Volume,
)

OUTPUT_DIR = Path("data/backtests/offline_demo")


def main() -> None:
    """
    Run the offline demo.
    """

    candles = _demo_candles()
    strategy = MovingAverageCrossoverStrategy(
        fast_period=3,
        slow_period=5,
    )
    sizer = FixedFractionPositionSizer(
        account_equity=Price(Decimal("1000")),
        risk_fraction=Decimal("0.02"),
        stop_loss_fraction=Decimal("0.05"),
    )
    risk_manager = SignalRiskManager(position_sizer=sizer)
    executor = PaperOrderExecutor(fee_rate=Decimal("0.001"))
    backtest = BacktestEngine(
        strategy=strategy,
        risk_manager=risk_manager,
        executor=executor,
        warmup_period=6,
    )

    result = backtest.run(candles)
    summary = PerformanceReporter().summarize(result.trades)
    CsvBacktestWriter(output_dir=OUTPUT_DIR).write(
        result=result,
        summary=summary,
    )

    print(f"signals={result.signal_count}")
    print(f"orders={result.order_count}")
    print(f"trades={result.trade_count}")
    print(f"net_pnl={summary.net_pnl}")
    print(f"output_dir={OUTPUT_DIR}")


def _demo_candles() -> tuple[Candle, ...]:
    close_values = (
        Decimal("100"),
        Decimal("99"),
        Decimal("98"),
        Decimal("97"),
        Decimal("98"),
        Decimal("99"),
        Decimal("101"),
        Decimal("103"),
        Decimal("104"),
        Decimal("102"),
        Decimal("100"),
        Decimal("98"),
        Decimal("96"),
    )

    return tuple(
        Candle(
            symbol=Symbol("BTC", "USDT"),
            timeframe=Timeframe("1h"),
            timestamp=datetime(2026, 7, 18, index, tzinfo=UTC),
            open_price=Price(close_value),
            high_price=Price(close_value),
            low_price=Price(close_value),
            close_price=Price(close_value),
            volume=Volume(Decimal("1")),
        )
        for index, close_value in enumerate(close_values)
    )


if __name__ == "__main__":
    main()
