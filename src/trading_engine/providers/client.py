class ExchangeClient:
    def fetch_ohlcv(self, symbol:str, timeframe:str, limit:int=500):
        raise NotImplementedError
