from datetime import UTC, datetime
from decimal import Decimal

import pytest

from quantforge.domain.enums import OrderSide, OrderStatus, OrderType
from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.models import Order
from quantforge.domain.value_objects import Price, Symbol, Volume


def test_create_market_order() -> None:
    order = Order(
        order_id=" order-1 ",
        symbol=Symbol("BTC", "USDT"),
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        quantity=Volume(Decimal("1")),
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
    )

    assert order.order_id == "order-1"
    assert order.status is OrderStatus.PENDING
    assert order.is_buy
    assert not order.is_sell


def test_create_limit_order() -> None:
    order = Order(
        order_id="order-1",
        symbol=Symbol("BTC", "USDT"),
        side=OrderSide.SELL,
        order_type=OrderType.LIMIT,
        quantity=Volume(Decimal("1")),
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
        price=Price(Decimal("100")),
    )

    assert order.price == Price(Decimal("100"))
    assert order.is_sell
    assert not order.is_buy


def test_empty_order_id() -> None:
    with pytest.raises(DomainValidationError):
        Order(
            order_id=" ",
            symbol=Symbol("BTC", "USDT"),
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=Volume(Decimal("1")),
            created_at=datetime(2026, 7, 18, tzinfo=UTC),
        )


def test_zero_order_quantity() -> None:
    with pytest.raises(DomainValidationError):
        Order(
            order_id="order-1",
            symbol=Symbol("BTC", "USDT"),
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=Volume(Decimal("0")),
            created_at=datetime(2026, 7, 18, tzinfo=UTC),
        )


def test_limit_order_requires_price() -> None:
    with pytest.raises(DomainValidationError):
        Order(
            order_id="order-1",
            symbol=Symbol("BTC", "USDT"),
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=Volume(Decimal("1")),
            created_at=datetime(2026, 7, 18, tzinfo=UTC),
        )


def test_market_order_cannot_define_price() -> None:
    with pytest.raises(DomainValidationError):
        Order(
            order_id="order-1",
            symbol=Symbol("BTC", "USDT"),
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=Volume(Decimal("1")),
            created_at=datetime(2026, 7, 18, tzinfo=UTC),
            price=Price(Decimal("100")),
        )
