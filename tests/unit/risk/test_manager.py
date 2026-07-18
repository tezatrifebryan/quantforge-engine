from datetime import UTC, datetime
from decimal import Decimal

from quantforge.domain.enums import OrderSide, OrderType
from quantforge.domain.value_objects import Price, Symbol, Volume
from quantforge.risk import SignalRiskManager
from quantforge.strategy import Signal, SignalAction


class FixedQuantitySizer:
    def calculate_quantity(self, entry_price: Price) -> Volume:
        return Volume(entry_price.value / Decimal("50"))


def test_buy_signal_creates_market_buy_order() -> None:
    manager = SignalRiskManager(
        position_sizer=FixedQuantitySizer(),
        order_id_factory=lambda: "order-1",
    )

    order = manager.create_order(_signal(SignalAction.BUY))

    assert order is not None
    assert order.order_id == "order-1"
    assert order.side is OrderSide.BUY
    assert order.order_type is OrderType.MARKET
    assert order.quantity == Volume(Decimal("2"))
    assert order.created_at == datetime(2026, 7, 18, tzinfo=UTC)


def test_sell_signal_creates_market_sell_order() -> None:
    manager = SignalRiskManager(
        position_sizer=FixedQuantitySizer(),
        order_id_factory=lambda: "order-1",
    )

    order = manager.create_order(_signal(SignalAction.SELL))

    assert order is not None
    assert order.side is OrderSide.SELL


def test_hold_signal_does_not_create_order() -> None:
    manager = SignalRiskManager(
        position_sizer=FixedQuantitySizer(),
        order_id_factory=lambda: "order-1",
    )

    order = manager.create_order(_signal(SignalAction.HOLD))

    assert order is None


def _signal(action: SignalAction) -> Signal:
    return Signal(
        symbol=Symbol("BTC", "USDT"),
        action=action,
        price=Price(Decimal("100")),
        generated_at=datetime(2026, 7, 18, tzinfo=UTC),
        reason="test",
    )
