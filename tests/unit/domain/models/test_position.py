from datetime import UTC, datetime
from decimal import Decimal

import pytest

from quantforge.domain.enums import PositionSide
from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.models import Position
from quantforge.domain.value_objects import Price, Symbol, Volume


def test_create_position() -> None:
    position = Position(
        position_id=" position-1 ",
        symbol=Symbol("BTC", "USDT"),
        side=PositionSide.LONG,
        quantity=Volume(Decimal("2")),
        entry_price=Price(Decimal("100")),
        opened_at=datetime(2026, 7, 18, tzinfo=UTC),
    )

    assert position.position_id == "position-1"
    assert position.notional == Price(Decimal("200"))


def test_empty_position_id() -> None:
    with pytest.raises(DomainValidationError):
        Position(
            position_id=" ",
            symbol=Symbol("BTC", "USDT"),
            side=PositionSide.LONG,
            quantity=Volume(Decimal("1")),
            entry_price=Price(Decimal("100")),
            opened_at=datetime(2026, 7, 18, tzinfo=UTC),
        )


def test_zero_position_quantity() -> None:
    with pytest.raises(DomainValidationError):
        Position(
            position_id="position-1",
            symbol=Symbol("BTC", "USDT"),
            side=PositionSide.LONG,
            quantity=Volume(Decimal("0")),
            entry_price=Price(Decimal("100")),
            opened_at=datetime(2026, 7, 18, tzinfo=UTC),
        )
