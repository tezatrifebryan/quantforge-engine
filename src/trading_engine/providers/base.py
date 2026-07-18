from typing import Protocol
from trading_engine.models.market_data import MarketData

class BaseProvider(Protocol):
    def get_market_data(self, symbol:str, timeframe:str, limit:int=500)->MarketData: ...
