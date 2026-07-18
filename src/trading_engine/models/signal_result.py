from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SignalResult:
    signal: str
    confidence: float
    entry: float|None=None
    stop_loss: float|None=None
    take_profit: float|None=None
