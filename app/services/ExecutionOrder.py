from abc import ABC

class ExecutionOrder(ABC):
    def __init__(self):
        pass
    
    def initialize(self):
        pass
    
    def preupdate(self):
        pass
    
    def update(self):
        pass
    
    def postupdate(self):
        pass