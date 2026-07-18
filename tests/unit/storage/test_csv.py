import csv
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from quantforge.backtest import BacktestResult
from quantforge.domain.enums import OrderSide
from quantforge.domain.models import Trade
from quantforge.domain.value_objects import Price, Symbol, Volume
from quantforge.reporting import PerformanceReporter
from quantforge.storage import CsvBacktestWriter


def test_csv_backtest_writer_writes_summary_and_trades(tmp_path: Path) -> None:
    trade = Trade(
        trade_id="trade-1",
        order_id="order-1",
        symbol=Symbol("BTC", "USDT"),
        side=OrderSide.BUY,
        price=Price(Decimal("100")),
        quantity=Volume(Decimal("2")),
        executed_at=datetime(2026, 7, 18, tzinfo=UTC),
        fee=Price(Decimal("0.2")),
    )
    result = BacktestResult(
        signals=(),
        orders=(),
        trades=(trade,),
    )
    summary = PerformanceReporter().summarize(result.trades)
    writer = CsvBacktestWriter(output_dir=tmp_path)

    writer.write(
        result=result,
        summary=summary,
    )

    with (tmp_path / "summary.csv").open(
        newline="",
        encoding="utf-8",
    ) as file:
        summary_rows = tuple(csv.DictReader(file))

    with (tmp_path / "trades.csv").open(
        newline="",
        encoding="utf-8",
    ) as file:
        trade_rows = tuple(csv.DictReader(file))

    assert summary_rows[0]["trade_count"] == "1"
    assert summary_rows[0]["net_pnl"] == "-0.2"
    assert trade_rows[0]["trade_id"] == "trade-1"
    assert trade_rows[0]["symbol"] == "BTC/USDT"
    assert trade_rows[0]["notional"] == "200"
