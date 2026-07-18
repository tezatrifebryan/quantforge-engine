from collections.abc import Sequence
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from quantforge.backtest import BacktestEngine, BacktestError
from quantforge.domain.value_objects import Candle, Price, Symbol, Timeframe, Volume
from quantforge.execution import PaperOrderExecutor
from quantforge.risk import SignalRiskManager
from quantforge.strategy import Signal, SignalAction


class SequenceStrategy:
    def __init__(self, actions: tuple[SignalAction, ...]) -> None:
        self._actions = actions
        self._index = 0

    def generate_signal(self, candles: Sequence[Candle]) -> Signal:
        action = self._actions[self._index]
        self._index += 1
        candle = candles[-1]

        return Signal(
            symbol=candle.symbol,
            action=action,
            price=candle.close_price,
            generated_at=candle.timestamp,
            reason="test",
        )


class FixedQuantitySizer:
    def calculate_quantity(self, entry_price: Price) -> Volume:
        return Volume(Decimal("2"))


class PriceBasedQuantitySizer:
    def calculate_quantity(self, entry_price: Price) -> Volume:
        return Volume(entry_price.value / Decimal("50"))


def test_backtest_runs_signals_orders_and_trades() -> None:
    engine = BacktestEngine(
        strategy=SequenceStrategy(
            actions=(
                SignalAction.HOLD,
                SignalAction.BUY,
            )
        ),
        risk_manager=SignalRiskManager(
            position_sizer=FixedQuantitySizer(),
            order_id_factory=lambda: "order-1",
        ),
        executor=PaperOrderExecutor(
            fee_rate=Decimal("0.001"),
            trade_id_factory=lambda: "trade-1",
        ),
        warmup_period=2,
    )

    result = engine.run(
        _candles(
            close_values=(
                Decimal("100"),
                Decimal("110"),
                Decimal("120"),
            )
        )
    )

    assert result.signal_count == 2
    assert result.order_count == 1
    assert result.trade_count == 1
    assert result.signals[0].action is SignalAction.HOLD
    assert result.orders[0].order_id == "order-1"
    assert result.trades[0].trade_id == "trade-1"
    assert result.trades[0].price == Price(Decimal("120"))
    assert result.trades[0].fee == Price(Decimal("0.240"))


def test_backtest_skips_sell_signal_without_open_quantity() -> None:
    engine = BacktestEngine(
        strategy=SequenceStrategy(
            actions=(
                SignalAction.SELL,
                SignalAction.HOLD,
            )
        ),
        risk_manager=SignalRiskManager(
            position_sizer=PriceBasedQuantitySizer(),
            order_id_factory=lambda: "order-1",
        ),
        executor=PaperOrderExecutor(
            trade_id_factory=lambda: "trade-1",
        ),
        warmup_period=2,
    )

    result = engine.run(
        _candles(
            close_values=(
                Decimal("100"),
                Decimal("110"),
                Decimal("120"),
            )
        )
    )

    assert result.signal_count == 2
    assert result.order_count == 0
    assert result.trade_count == 0


def test_backtest_clamps_sell_order_to_open_quantity() -> None:
    engine = BacktestEngine(
        strategy=SequenceStrategy(
            actions=(
                SignalAction.BUY,
                SignalAction.SELL,
            )
        ),
        risk_manager=SignalRiskManager(
            position_sizer=PriceBasedQuantitySizer(),
            order_id_factory=lambda: "order-1",
        ),
        executor=PaperOrderExecutor(
            trade_id_factory=lambda: "trade-1",
        ),
        warmup_period=2,
    )

    result = engine.run(
        _candles(
            close_values=(
                Decimal("100"),
                Decimal("110"),
                Decimal("120"),
            )
        )
    )

    assert result.order_count == 2
    assert result.orders[0].quantity == Volume(Decimal("2.2"))
    assert result.orders[1].quantity == Volume(Decimal("2.2"))
    assert result.trades[1].quantity == Volume(Decimal("2.2"))


def test_warmup_period_must_be_greater_than_zero() -> None:
    with pytest.raises(BacktestError):
        BacktestEngine(
            strategy=SequenceStrategy(actions=(SignalAction.HOLD,)),
            risk_manager=SignalRiskManager(
                position_sizer=FixedQuantitySizer(),
            ),
            executor=PaperOrderExecutor(),
            warmup_period=0,
        )


def test_backtest_requires_enough_candles() -> None:
    engine = BacktestEngine(
        strategy=SequenceStrategy(actions=(SignalAction.HOLD,)),
        risk_manager=SignalRiskManager(
            position_sizer=FixedQuantitySizer(),
        ),
        executor=PaperOrderExecutor(),
        warmup_period=3,
    )

    with pytest.raises(BacktestError):
        engine.run(
            _candles(
                close_values=(
                    Decimal("100"),
                    Decimal("110"),
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
