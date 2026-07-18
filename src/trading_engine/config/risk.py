from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class RiskConfig:
    risk_per_trade:float=0.01
    max_open_positions:int=3
