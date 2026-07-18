from decimal import Decimal

import pytest

from quantforge.domain.value_objects import Price, Volume
from quantforge.risk import FixedFractionPositionSizer, RiskError


def test_fixed_fraction_position_sizer_calculates_quantity() -> None:
    sizer = FixedFractionPositionSizer(
        account_equity=Price(Decimal("1000")),
        risk_fraction=Decimal("0.02"),
        stop_loss_fraction=Decimal("0.05"),
    )

    quantity = sizer.calculate_quantity(
        entry_price=Price(Decimal("100")),
    )

    assert quantity == Volume(Decimal("4"))


def test_account_equity_must_be_greater_than_zero() -> None:
    with pytest.raises(RiskError):
        FixedFractionPositionSizer(
            account_equity=Price(Decimal("0")),
            risk_fraction=Decimal("0.02"),
            stop_loss_fraction=Decimal("0.05"),
        )


def test_risk_fraction_must_be_greater_than_zero() -> None:
    with pytest.raises(RiskError):
        FixedFractionPositionSizer(
            account_equity=Price(Decimal("1000")),
            risk_fraction=Decimal("0"),
            stop_loss_fraction=Decimal("0.05"),
        )


def test_stop_loss_fraction_must_be_at_most_one() -> None:
    with pytest.raises(RiskError):
        FixedFractionPositionSizer(
            account_equity=Price(Decimal("1000")),
            risk_fraction=Decimal("0.02"),
            stop_loss_fraction=Decimal("1.1"),
        )


def test_entry_price_must_be_greater_than_zero() -> None:
    sizer = FixedFractionPositionSizer(
        account_equity=Price(Decimal("1000")),
        risk_fraction=Decimal("0.02"),
        stop_loss_fraction=Decimal("0.05"),
    )

    with pytest.raises(RiskError):
        sizer.calculate_quantity(
            entry_price=Price(Decimal("0")),
        )
