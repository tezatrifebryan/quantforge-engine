from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class IndicatorConfig:
    ema_fast:int=20
    ema_slow:int=50
    ema_trend:int=200
