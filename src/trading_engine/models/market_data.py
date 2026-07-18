from dataclasses import dataclass
from .candle import Candle

@dataclass(frozen=True, slots=True)
class MarketData:
    symbol: str
    timeframe: str
    candles: list[Candle]
