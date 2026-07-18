from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TrendResult:
    direction: str
    strength: float
