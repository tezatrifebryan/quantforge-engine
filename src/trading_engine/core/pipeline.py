from typing import Callable, Any

class Pipeline:
    def __init__(self)->None:
        self._steps:list[Callable[[Any],Any]]=[]

    def add(self,step:Callable[[Any],Any])->None:
        self._steps.append(step)

    def run(self,data:Any)->Any:
        result=data
        for step in self._steps:
            result=step(result)
        return result
