class Classification:
    id: int = 0
    def __init__(self, label: str, value: str, info: str = ""):
        self.label: str = label
        self.value: str = value
        self.info: bool = info
        self.id += 1

    def __str__(self):
        return f"({self.label}) {self.value}"

    def __repr__(self):
        return f"Classification({self.value})"
        
    def __eq__(self, other):
        return self.label == other.label and self.value == other.value