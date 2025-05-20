from typing import Generic, TypeVar
from random import shuffle

TData = TypeVar('TData')  # Declare a type variable
class Randomizable(Generic[TData]):
    def randomize(self):
        shuffle(self.randomized_index)
        return self.get_randomized_data()
    
    def set_value(self, *args):
        self.data: tuple[TData] = args
        self.length: int = len(self.data)
        self.randomized_index: list[int] = [i for i in range(self.length)]
        self.randomize()
        
    def get_randomized_data(self):
        return [self.data[i] for i in self.randomized_index]
    
    def get_randomized_index(self, index: int):
        return self.data[self.randomized_index[index]]