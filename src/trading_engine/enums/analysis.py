from enum import Enum
class TrendDirection(str,Enum): BULLISH='bullish';BEARISH='bearish';SIDEWAYS='sideways'
class MarketStructure(str,Enum): UPTREND='uptrend';DOWNTREND='downtrend';RANGE='range'
