from datetime import UTC, datetime
from decimal import Decimal

import pytest

from quantforge.domain.enums import OrderSide
from quantforge.domain.models import Trade
from quantforge.domain.value_objects import Price, Symbol, Volume
from quantforge.reporting import PerformanceReporter, ReportingError


def test_performance_summary_calculates_realized_profit() -> None:
    reporter = PerformanceReporter()

    summary = reporter.summarize(
        trades=(
            _trade(
                trade_id="trade-1",
                side=OrderSide.BUY,
                price=Decimal("100"),
                quantity=Decimal("2"),
                fee=Decimal("0.2"),
            ),
            _trade(
                trade_id="trade-2",
                side=OrderSide.SELL,
                price=Decimal("120"),
                quantity=Decimal("2"),
                fee=Decimal("0.24"),
            ),
        )
    )

    assert summary.trade_count == 2
    assert summary.closed_trade_count == 1
    assert summary.winning_trade_count == 1
    assert summary.open_quantity == Decimal("0")
    assert summary.average_entry_price == Decimal("0")
    assert summary.gross_pnl == Decimal("40")
    assert summary.total_fees == Decimal("0.44")
    assert summary.net_pnl == Decimal("39.56")
    assert summary.win_rate == Decimal("100")


def test_performance_summary_calculates_realized_loss() -> None:
    reporter = PerformanceReporter()

    summary = reporter.summarize(
        trades=(
            _trade(
                trade_id="trade-1",
                side=OrderSide.BUY,
                price=Decimal("100"),
                quantity=Decimal("1"),
            ),
            _trade(
                trade_id="trade-2",
                side=OrderSide.SELL,
                price=Decimal("90"),
                quantity=Decimal("1"),
            ),
        )
    )

    assert summary.gross_pnl == Decimal("-10")
    assert summary.net_pnl == Decimal("-10")
    assert summary.win_rate == Decimal("0")


def test_performance_summary_tracks_weighted_average_entry() -> None:
    reporter = PerformanceReporter()

    summary = reporter.summarize(
        trades=(
            _trade(
                trade_id="trade-1",
                side=OrderSide.BUY,
                price=Decimal("100"),
                quantity=Decimal("1"),
            ),
            _trade(
                trade_id="trade-2",
                side=OrderSide.BUY,
                price=Decimal("200"),
                quantity=Decimal("1"),
            ),
            _trade(
                trade_id="trade-3",
                side=OrderSide.SELL,
                price=Decimal("180"),
                quantity=Decimal("1"),
            ),
        )
    )

    assert summary.gross_pnl == Decimal("30")
    assert summary.open_quantity == Decimal("1")
    assert summary.average_entry_price == Decimal("150")


def test_performance_summary_with_no_closed_trades_has_zero_win_rate() -> None:
    reporter = PerformanceReporter()

    summary = reporter.summarize(
        trades=(
            _trade(
                trade_id="trade-1",
                side=OrderSide.BUY,
                price=Decimal("100"),
                quantity=Decimal("1"),
            ),
        )
    )

    assert summary.closed_trade_count == 0
    assert summary.win_rate == Decimal("0")


def test_sell_trade_cannot_exceed_open_quantity() -> None:
    reporter = PerformanceReporter()

    with pytest.raises(ReportingError):
        reporter.summarize(
            trades=(
                _trade(
                    trade_id="trade-1",
                    side=OrderSide.SELL,
                    price=Decimal("100"),
                    quantity=Decimal("1"),
                ),
            )
        )


def _trade(
    trade_id: str,
    side: OrderSide,
    price: Decimal,
    quantity: Decimal,
    fee: Decimal = Decimal("0"),
) -> Trade:
    return Trade(
        trade_id=trade_id,
        order_id=f"order-{trade_id}",
        symbol=Symbol("BTC", "USDT"),
        side=side,
        price=Price(price),
        quantity=Volume(quantity),
        executed_at=datetime(2026, 7, 18, tzinfo=UTC),
        fee=Price(fee),
    )
