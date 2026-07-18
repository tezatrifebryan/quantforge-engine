from datetime import UTC, datetime
from decimal import Decimal

import pytest

from quantforge.domain.enums import OrderSide, OrderStatus, OrderType
from quantforge.domain.models import Order
from quantforge.domain.value_objects import Price, Symbol, Volume
from quantforge.execution import ExecutionError, PaperOrderExecutor


def test_execute_market_order_at_market_price() -> None:
    executor = PaperOrderExecutor(
        fee_rate=Decimal("0.001"),
        trade_id_factory=lambda: "trade-1",
    )
    executed_at = datetime(2026, 7, 18, tzinfo=UTC)

    trade = executor.execute(
        order=_market_order(),
        market_price=Price(Decimal("100")),
        executed_at=executed_at,
    )

    assert trade.trade_id == "trade-1"
    assert trade.order_id == "order-1"
    assert trade.price == Price(Decimal("100"))
    assert trade.quantity == Volume(Decimal("2"))
    assert trade.executed_at == executed_at
    assert trade.fee == Price(Decimal("0.200"))


def test_execute_limit_order_at_limit_price() -> None:
    executor = PaperOrderExecutor(
        trade_id_factory=lambda: "trade-1",
    )

    trade = executor.execute(
        order=Order(
            order_id="order-1",
            symbol=Symbol("BTC", "USDT"),
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=Volume(Decimal("2")),
            created_at=datetime(2026, 7, 18, tzinfo=UTC),
            price=Price(Decimal("95")),
        )
    )

    assert trade.price == Price(Decimal("95"))
    assert trade.fee == Price(Decimal("0"))


def test_market_order_requires_market_price() -> None:
    executor = PaperOrderExecutor()

    with pytest.raises(ExecutionError):
        executor.execute(
            order=_market_order(),
        )


def test_only_pending_orders_can_be_executed() -> None:
    executor = PaperOrderExecutor()

    with pytest.raises(ExecutionError):
        executor.execute(
            order=Order(
                order_id="order-1",
                symbol=Symbol("BTC", "USDT"),
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                quantity=Volume(Decimal("2")),
                created_at=datetime(2026, 7, 18, tzinfo=UTC),
                status=OrderStatus.CANCELED,
            ),
            market_price=Price(Decimal("100")),
        )


def test_fee_rate_must_be_between_zero_and_one() -> None:
    with pytest.raises(ExecutionError):
        PaperOrderExecutor(
            fee_rate=Decimal("1.1"),
        )


def _market_order() -> Order:
    return Order(
        order_id="order-1",
        symbol=Symbol("BTC", "USDT"),
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        quantity=Volume(Decimal("2")),
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
    )
