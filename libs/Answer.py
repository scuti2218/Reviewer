class Answer:
    id: int = 0
    def __init__(self, value: str, is_correct: bool):
        self.value: str = value
        self.is_correct: bool = is_correct
        self.id += 1

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"Answer({self.value})"
        
    def __eq__(self, other):
        return self.value == other.value