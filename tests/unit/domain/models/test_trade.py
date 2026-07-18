from datetime import UTC, datetime
from decimal import Decimal

import pytest

from quantforge.domain.enums import OrderSide
from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.models import Trade
from quantforge.domain.value_objects import Price, Symbol, Volume


def test_create_trade() -> None:
    trade = Trade(
        trade_id=" trade-1 ",
        order_id=" order-1 ",
        symbol=Symbol("BTC", "USDT"),
        side=OrderSide.BUY,
        price=Price(Decimal("100")),
        quantity=Volume(Decimal("2")),
        executed_at=datetime(2026, 7, 18, tzinfo=UTC),
    )

    assert trade.trade_id == "trade-1"
    assert trade.order_id == "order-1"
    assert trade.fee == Price(Decimal("0"))
    assert trade.notional == Price(Decimal("200"))


def test_empty_trade_id() -> None:
    with pytest.raises(DomainValidationError):
        Trade(
            trade_id=" ",
            order_id="order-1",
            symbol=Symbol("BTC", "USDT"),
            side=OrderSide.BUY,
            price=Price(Decimal("100")),
            quantity=Volume(Decimal("1")),
            executed_at=datetime(2026, 7, 18, tzinfo=UTC),
        )


def test_empty_trade_order_id() -> None:
    with pytest.raises(DomainValidationError):
        Trade(
            trade_id="trade-1",
            order_id=" ",
            symbol=Symbol("BTC", "USDT"),
            side=OrderSide.BUY,
            price=Price(Decimal("100")),
            quantity=Volume(Decimal("1")),
            executed_at=datetime(2026, 7, 18, tzinfo=UTC),
        )


def test_zero_trade_quantity() -> None:
    with pytest.raises(DomainValidationError):
        Trade(
            trade_id="trade-1",
            order_id="order-1",
            symbol=Symbol("BTC", "USDT"),
            side=OrderSide.BUY,
            price=Price(Decimal("100")),
            quantity=Volume(Decimal("0")),
            executed_at=datetime(2026, 7, 18, tzinfo=UTC),
        )
