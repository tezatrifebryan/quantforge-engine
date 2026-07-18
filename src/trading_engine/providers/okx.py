from .client import ExchangeClient

class OkxProvider:
    def __init__(self, client:ExchangeClient):
        self.client=client

    def fetch(self, symbol:str, timeframe:str, limit:int=500):
        return self.client.fetch_ohlcv(symbol,timeframe,limit)
