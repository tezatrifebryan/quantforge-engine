from trading_engine.providers.factory import ProviderFactory
from trading_engine.providers.client import ExchangeClient

class Dummy(ExchangeClient):
    def fetch_ohlcv(self,*args,**kwargs):
        return []

def test_factory():
    p=ProviderFactory.create("okx",Dummy())
    assert p is not None
