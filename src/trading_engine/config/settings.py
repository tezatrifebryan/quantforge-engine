from dataclasses import dataclass,field
from .exchange import ExchangeConfig
from .risk import RiskConfig
from .indicator import IndicatorConfig
from .strategy import StrategyConfig
from .logging import LoggingConfig

@dataclass(frozen=True,slots=True)
class Settings:
    exchange:ExchangeConfig=field(default_factory=ExchangeConfig)
    risk:RiskConfig=field(default_factory=RiskConfig)
    indicator:IndicatorConfig=field(default_factory=IndicatorConfig)
    strategy:StrategyConfig=field(default_factory=StrategyConfig)
    logging:LoggingConfig=field(default_factory=LoggingConfig)
