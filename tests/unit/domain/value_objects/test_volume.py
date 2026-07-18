from decimal import Decimal

import pytest

from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.value_objects import Volume


def test_create_volume() -> None:
    volume = Volume(Decimal("100.5"))

    assert volume.value == Decimal("100.5")


def test_negative_volume() -> None:
    with pytest.raises(DomainValidationError):
        Volume(Decimal("-1"))


def test_add_volume() -> None:
    v1 = Volume(Decimal("10"))
    v2 = Volume(Decimal("5"))

    assert (v1 + v2).value == Decimal("15")


def test_subtract_volume() -> None:
    v1 = Volume(Decimal("10"))
    v2 = Volume(Decimal("3"))

    assert (v1 - v2).value == Decimal("7")


def test_compare_volume() -> None:
    v1 = Volume(Decimal("100"))
    v2 = Volume(Decimal("200"))

    assert v2 > v1
    assert v1 < v2
