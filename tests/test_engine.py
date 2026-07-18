from trading_engine.core.bootstrap import create_engine

def test_engine():
    e=create_engine()
    assert e.run(1)==1
