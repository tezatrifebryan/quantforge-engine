from enum import Enum
class SignalType(str,Enum): BUY='buy';SELL='sell';NONE='none'
class OrderSide(str,Enum): LONG='long';SHORT='short'
