class ProviderRegistry:
    def __init__(self):
        self._providers={}
    def register(self,name,provider):
        self._providers[name]=provider
    def get(self,name):
        return self._providers[name]
