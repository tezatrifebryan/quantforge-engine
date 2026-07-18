from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BacktestResult:
    total_trades:int
    win_rate:float
    profit_factor:float
