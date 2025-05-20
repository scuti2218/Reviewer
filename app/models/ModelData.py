from abc import ABC, abstractmethod

class ModelData(ABC):
    def __init__(self, **kwargs):
        self.title = ""
        self.info = ""
        self.set_json(**kwargs)
    
    @abstractmethod
    def show(self):
        pass
    
    def set_json(self, **kwargs):
        for key, value in kwargs.items():
            if key in vars(self).keys():
                setattr(self, key, value)
        return self
                
    def get_json(self):
        return self.__dict__