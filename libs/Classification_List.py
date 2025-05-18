from .Classification import Classification

class Classification_List:
    def __init__(self):
        self.values: list[Classification] = []
            
    # SETTERS
    def set_value(self, classification: list[Classification]):
        self.values += classification
    
    def add_value(self, classification: Classification):
        self.values.append(classification)
        
    def get_by_label(self, label: str):
        for i in self.values:
            if i.label == label:
                return i
        return None
        
    def get_by_name(self, name: str):
        for i in self.values:
            if i.value == name:
                return i
        return None
    
    def check_classification_by_label(self, label: str):
        for i in self.values:
            if i.label == label:
                return True
        return False
    
    def check_classification_by_name(self, name: str):
        for i in self.values:
            if i.value == name:
                return True
        return False