"""Simple dependency container."""
from typing import Any

class Container:
    def __init__(self)->None:
        self._services:dict[str,Any]={}

    def register(self,name:str,service:Any)->None:
        self._services[name]=service

    def resolve(self,name:str)->Any:
        return self._services[name]
