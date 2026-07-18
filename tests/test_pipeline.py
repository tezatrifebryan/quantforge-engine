from trading_engine.core.pipeline import Pipeline

def test_pipeline():
    p=Pipeline()
    p.add(lambda x:x+1)
    p.add(lambda x:x*2)
    assert p.run(3)==8
