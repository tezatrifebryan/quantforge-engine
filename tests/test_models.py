from datetime import datetime
from trading_engine.models.candle import Candle

def test_candle():
    c=Candle(datetime.now(),1,2,0.5,1.5,100)
    assert c.close==1.5
