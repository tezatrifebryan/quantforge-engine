from datetime import timedelta

import pytest

from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.value_objects import Timeframe


def test_create_timeframe() -> None:
    timeframe = Timeframe("1H")

    assert timeframe.value == "1h"
    assert str(timeframe) == "1h"


def test_timeframe_duration() -> None:
    timeframe = Timeframe("15m")

    assert timeframe.duration == timedelta(minutes=15)


def test_unsupported_timeframe() -> None:
    with pytest.raises(DomainValidationError):
        Timeframe("2h")
