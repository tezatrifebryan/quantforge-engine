"""
CSV storage for backtest artifacts.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from quantforge.backtest import BacktestResult
from quantforge.domain.models import Trade
from quantforge.reporting import PerformanceSummary
from quantforge.storage.exceptions import StorageError

SUMMARY_FIELDS = (
    "trade_count",
    "closed_trade_count",
    "winning_trade_count",
    "open_quantity",
    "average_entry_price",
    "gross_pnl",
    "total_fees",
    "net_pnl",
    "win_rate",
)

TRADE_FIELDS = (
    "trade_id",
    "order_id",
    "symbol",
    "side",
    "price",
    "quantity",
    "executed_at",
    "fee",
    "notional",
)


@dataclass(frozen=True, slots=True)
class CsvBacktestWriter:
    """
    Write backtest result artifacts to CSV files.
    """

    output_dir: Path

    def write(
        self,
        result: BacktestResult,
        summary: PerformanceSummary,
    ) -> None:
        """
        Write summary and trades CSV files.
        """

        try:
            self.output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )
            _write_summary(
                path=self.output_dir / "summary.csv",
                summary=summary,
            )
            _write_trades(
                path=self.output_dir / "trades.csv",
                trades=result.trades,
            )
        except OSError as exc:
            raise StorageError("Backtest CSV output could not be written.") from exc


def _write_summary(path: Path, summary: PerformanceSummary) -> None:
    with path.open(
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=SUMMARY_FIELDS,
        )
        writer.writeheader()
        writer.writerow(
            {
                "trade_count": summary.trade_count,
                "closed_trade_count": summary.closed_trade_count,
                "winning_trade_count": summary.winning_trade_count,
                "open_quantity": str(summary.open_quantity),
                "average_entry_price": str(summary.average_entry_price),
                "gross_pnl": str(summary.gross_pnl),
                "total_fees": str(summary.total_fees),
                "net_pnl": str(summary.net_pnl),
                "win_rate": str(summary.win_rate),
            }
        )


def _write_trades(path: Path, trades: tuple[Trade, ...]) -> None:
    with path.open(
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=TRADE_FIELDS,
        )
        writer.writeheader()
        writer.writerows(_trade_row(trade) for trade in trades)


def _trade_row(trade: Trade) -> dict[str, str]:
    return {
        "trade_id": trade.trade_id,
        "order_id": trade.order_id,
        "symbol": str(trade.symbol),
        "side": trade.side.value,
        "price": str(trade.price.value),
        "quantity": str(trade.quantity.value),
        "executed_at": trade.executed_at.isoformat(),
        "fee": str(trade.fee.value),
        "notional": str(trade.notional.value),
    }
