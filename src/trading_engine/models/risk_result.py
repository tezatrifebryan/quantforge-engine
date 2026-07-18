from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RiskResult:
    risk: float
    reward: float
    rr_ratio: float
