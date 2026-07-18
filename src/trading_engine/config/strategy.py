from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class StrategyConfig:
    min_rr:float=2.0
    confirmation_candles:int=1
