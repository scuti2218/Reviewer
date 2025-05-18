from .Classification_List import Classification_List
from .Classification import Classification

class Score:
    def __init__(self, max: int, value: int = 0):
        self.__locked = False
        self.set_whole(max, value)
        self.classifications: dict[str, int] = {}
        self.classifications_max: dict[str, int] = {}

    def __str__(self):
        return self.show()

    def __repr__(self):
        return self.show()
    
    def show(self):
        return f"Score: {self.__value} / {self.__max} ({self.get_percentage(self.__value, self.__max)}%)"
    
    def print(self):
        print(self.show())
        
    def update_classification_max(self, classification: str):
        if classification in self.classifications_max.keys():
            self.classifications_max[classification] += 1
        else:
            self.classifications_max[classification] = 1
        
    def print_classification(self, classifications: Classification_List):
        for label, max_score in self.classifications_max.items():
            classification: Classification = classifications.get_by_label(label)
            cur_score = 0
            if label in self.classifications:
                cur_score = self.classifications[label]
            print(f"\t({classification.label}) {classification.value} = {cur_score} / {max_score} ({self.get_percentage(cur_score, max_score)}%)")

    def get_percentage(self, value, max):
        return (value * 100) / max
        
    def get_value(self):
        return self.__value
    
    def get_max(self):
        return self.__max
    
    # LOCKER
    def lock(self):
        if self.__locked:
            print("Score is Final!")
            return
        self.__locked = True
    
    # SETTERS
    def set_whole(self, max: int, value: int):
        if self.__locked:
            print("Score is Final!")
            return
        self.__value = value
        self.__max = max
    
    def set_max(self, max: int):
        if self.__locked:
            print("Score is Final!")
            return
        self.__max == max
        
    def add_max(self, max: int):
        if self.__locked:
            print("Score is Final!")
            return
        self.__max += 1
    
    def add(self, classification: str):
        if self.__locked:
            print("Score is Final!")
            return
        if self.__value == self.__max:
            print("Score is maxed!")
        else:
            self.__value += 1
            if classification in self.classifications.keys():
                self.classifications[classification] += 1
            else:
                self.classifications[classification] = 1
            
    def remove(self, classification: str):
        if self.__locked:
            print("Score is Final!")
            return
        if self.__value == 0:
            print("Score is none!")
        else:
            self.__value -= 1
            self.classifications[classification] -= 1