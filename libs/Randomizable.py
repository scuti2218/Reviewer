from typing import Generic, TypeVar
from random import shuffle

TData = TypeVar('TData')  # Declare a type variable
class Randomizable(Generic[TData]):
    def __init__(self):
        self.arrangement: list[int] = []
        self.data: list[TData] = []
        self.length: int = 0
        
    def update_data(self):
        self.length = len(self.data)
        self.arrangement = list(range(len(self.data)))
    
    def randomize(self):
        self.update_data()
        shuffle(self.arrangement)
        
    def get_randomized_data(self) -> list[TData]:
        return [self.data[i] for i in self.arrangement]
    
    def get_real_index(self, index: int) -> int:
        return self.arrangement[index]
    
    def get_from_randomized(self, index: int) -> TData:
        return self.data[self.get_real_index(index)]