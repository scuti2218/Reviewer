class Score:
    def __init__(self, max: int, value: int = 0):
        self.__value = value
        self.__max = max
        self.__locked = False

    def __str__(self):
        return self.show()

    def __repr__(self):
        return self.show()
    
    def show(self):
        return f"Score: {self.__value} / {self.__max}"
    
    def print(self):
        print(self.show())
        
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
    
    def add(self):
        if self.__locked:
            print("Score is Final!")
            return
        if self.__value == self.__max:
            print("Score is maxed!")
        else:
            self.__value += 1
            
    def remove(self):
        if self.__locked:
            print("Score is Final!")
            return
        if self.__value == 0:
            print("Score is none!")
        else:
            self.__value -= 1