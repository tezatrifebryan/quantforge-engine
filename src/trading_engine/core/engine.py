from .container import Container
from .pipeline import Pipeline

class TradingEngine:
    def __init__(self,container:Container|None=None)->None:
        self.container=container or Container()
        self.pipeline=Pipeline()

    def register(self,name:str,service:object)->None:
        self.container.register(name,service)

    def add_step(self,step)->None:
        self.pipeline.add(step)

    def run(self,data):
        return self.pipeline.run(data)
