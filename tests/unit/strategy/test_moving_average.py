from datetime import UTC
from datetime import datetime
from decimal import Decimal

import pytest

from quantforge.domain.value_objects import Candle
from quantforge.domain.value_objects import Price
from quantforge.domain.value_objects import Symbol
from quantforge.domain.value_objects import Timeframe
from quantforge.domain.value_objects import Volume
from quantforge.strategy import MovingAverageCrossoverStrategy
from quantforge.strategy import SignalAction
from quantforge.strategy import StrategyError


def test_generate_buy_signal_when_fast_average_crosses_above_slow_average() -> None:
    strategy = MovingAverageCrossoverStrategy(
        fast_period=2,
        slow_period=3,
    )

    signal = strategy.generate_signal(
        _candles(
            close_values=(
                Decimal("10"),
                Decimal("9"),
                Decimal("8"),
                Decimal("9"),
                Decimal("10"),
            )
        )
    )

    assert signal.action is SignalAction.BUY
    assert signal.price == Price(Decimal("10"))
    assert signal.reason == "fast_ma_crossed_above_slow_ma"


def test_generate_sell_signal_when_fast_average_crosses_below_slow_average() -> None:
    strategy = MovingAverageCrossoverStrategy(
        fast_period=2,
        slow_period=3,
    )

    signal = strategy.generate_signal(
        _candles(
            close_values=(
                Decimal("8"),
                Decimal("9"),
                Decimal("10"),
                Decimal("9"),
                Decimal("8"),
            )
        )
    )

    assert signal.action is SignalAction.SELL
    assert signal.price == Price(Decimal("8"))
    assert signal.reason == "fast_ma_crossed_below_slow_ma"


def test_generate_hold_signal_when_no_crossover_exists() -> None:
    strategy = MovingAverageCrossoverStrategy(
        fast_period=2,
        slow_period=3,
    )

    signal = strategy.generate_signal(
        _candles(
            close_values=(
                Decimal("10"),
                Decimal("11"),
                Decimal("12"),
                Decimal("13"),
                Decimal("14"),
            )
        )
    )

    assert signal.action is SignalAction.HOLD
    assert signal.price == Price(Decimal("14"))
    assert signal.reason == "no_moving_average_crossover"


def test_fast_period_must_be_lower_than_slow_period() -> None:
    with pytest.raises(StrategyError):
        MovingAverageCrossoverStrategy(
            fast_period=3,
            slow_period=3,
        )


def test_strategy_requires_enough_candles_to_detect_crossover() -> None:
    strategy = MovingAverageCrossoverStrategy(
        fast_period=2,
        slow_period=3,
    )

    with pytest.raises(StrategyError):
        strategy.generate_signal(
            _candles(
                close_values=(
                    Decimal("10"),
                    Decimal("11"),
                    Decimal("12"),
                )
            )
        )


def _candles(close_values: tuple[Decimal, ...]) -> tuple[Candle, ...]:
    return tuple(
        Candle(
            symbol=Symbol("BTC", "USDT"),
            timeframe=Timeframe("1h"),
            timestamp=datetime(2026, 7, 18, index, tzinfo=UTC),
            open_price=Price(close_value),
            high_price=Price(close_value),
            low_price=Price(close_value),
            close_price=Price(close_value),
            volume=Volume(Decimal("1")),
        )
        for index, close_value in enumerate(close_values)
    )
