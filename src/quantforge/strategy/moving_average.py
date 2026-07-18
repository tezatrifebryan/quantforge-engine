"""
Moving average crossover strategy.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from quantforge.domain.value_objects import Candle
from quantforge.indicators import IndicatorError, SimpleMovingAverage
from quantforge.strategy.exceptions import StrategyError
from quantforge.strategy.signal import Signal, SignalAction

MINIMUM_CROSSOVER_POINTS = 2
BUY_REASON = "fast_ma_crossed_above_slow_ma"
SELL_REASON = "fast_ma_crossed_below_slow_ma"
HOLD_REASON = "no_moving_average_crossover"


@dataclass(frozen=True, slots=True)
class MovingAverageCrossoverStrategy:
    """
    Moving average crossover strategy.
    """

    fast_period: int
    slow_period: int

    def __post_init__(self) -> None:
        """
        Validate strategy periods.
        """

        if self.fast_period >= self.slow_period:
            raise StrategyError("Fast period must be lower than slow period.")

    def generate_signal(self, candles: Sequence[Candle]) -> Signal:
        """
        Generate buy, sell, or hold signal from moving average crossover.
        """

        if len(candles) < self.slow_period + 1:
            raise StrategyError("Not enough candles to detect crossover.")

        try:
            fast_values = SimpleMovingAverage(self.fast_period).calculate(candles)
            slow_values = SimpleMovingAverage(self.slow_period).calculate(candles)
        except IndicatorError as exc:
            raise StrategyError("Strategy indicators could not be calculated.") from exc

        if len(slow_values) < MINIMUM_CROSSOVER_POINTS:
            raise StrategyError("Not enough indicator values to detect crossover.")

        previous_fast = fast_values[-MINIMUM_CROSSOVER_POINTS]
        current_fast = fast_values[-1]
        previous_slow = slow_values[-MINIMUM_CROSSOVER_POINTS]
        current_slow = slow_values[-1]
        last_candle = candles[-1]

        if previous_fast <= previous_slow and current_fast > current_slow:
            return Signal(
                symbol=last_candle.symbol,
                action=SignalAction.BUY,
                price=last_candle.close_price,
                generated_at=last_candle.timestamp,
                reason=BUY_REASON,
            )

        if previous_fast >= previous_slow and current_fast < current_slow:
            return Signal(
                symbol=last_candle.symbol,
                action=SignalAction.SELL,
                price=last_candle.close_price,
                generated_at=last_candle.timestamp,
                reason=SELL_REASON,
            )

        return Signal(
            symbol=last_candle.symbol,
            action=SignalAction.HOLD,
            price=last_candle.close_price,
            generated_at=last_candle.timestamp,
            reason=HOLD_REASON,
        )
