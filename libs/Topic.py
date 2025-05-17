from .Printer import print_question

class Topic:
    def __init__(self, title: str, info: str, dir: str):
        self.title = title
        self.info = info
        self.dir = dir

    def __str__(self):
        return self.show()

    def __repr__(self):
        return self.show()
    
    def show(self):
        return f"{self.title} : {self.info}"
    
    def print(self, count: int):
        print_question(f"{self.title} : {self.info}", count)