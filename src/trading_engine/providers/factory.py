from .okx import OkxProvider
from .client import ExchangeClient

class ProviderFactory:
    @staticmethod
    def create(exchange:str, client:ExchangeClient):
        exchange=exchange.lower()
        if exchange=="okx":
            return OkxProvider(client)
        raise ValueError(f"Unsupported exchange: {exchange}")
