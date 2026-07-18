from decimal import Decimal

import pytest

from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.value_objects import Price


def test_create_price() -> None:
    price = Price(Decimal("100"))

    assert price.value == Decimal("100")


def test_negative_price() -> None:
    with pytest.raises(DomainValidationError):
        Price(Decimal("-1"))


def test_add_price() -> None:
    p1 = Price(Decimal("10"))
    p2 = Price(Decimal("5"))

    assert (p1 + p2).value == Decimal("15")


def test_subtract_price() -> None:
    p1 = Price(Decimal("10"))
    p2 = Price(Decimal("3"))

    assert (p1 - p2).value == Decimal("7")


def test_compare_price() -> None:
    p1 = Price(Decimal("100"))
    p2 = Price(Decimal("200"))

    assert p2 > p1
    assert p1 < p2
