from enum import Enum
class Exchange(str,Enum): OKX='okx';BINANCE='binance';BYBIT='bybit';BITGET='bitget'
class Timeframe(str,Enum): M5='5m';M15='15m';H1='1h';H4='4h';D1='1d'
