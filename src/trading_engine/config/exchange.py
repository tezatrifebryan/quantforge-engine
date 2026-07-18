from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class ExchangeConfig:
    name:str="okx"
    market_type:str="swap"
