from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True, slots=True)
class TradeResult:
    trade_id: UUID = uuid4()
    symbol: str = ""
    side: str = ""
    entry: float = 0.0
