from quantforge.domain.enums import OrderSide, OrderStatus, OrderType


def test_order_side_values() -> None:
    assert OrderSide.BUY.value == "buy"
    assert OrderSide.SELL.value == "sell"


def test_order_type_values() -> None:
    assert OrderType.MARKET.value == "market"
    assert OrderType.LIMIT.value == "limit"


def test_order_status_values() -> None:
    assert OrderStatus.PENDING.value == "pending"
    assert OrderStatus.OPEN.value == "open"
    assert OrderStatus.FILLED.value == "filled"
    assert OrderStatus.CANCELED.value == "canceled"
    assert OrderStatus.REJECTED.value == "rejected"
