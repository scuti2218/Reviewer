from ..views import View
from ..models import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model
        self.commands: dict[str, function] = {}
        self.initialize()
        
    def initialize(self):
        self.view.initialize()
        self.model.initialize()
        
        self.commands["sample"] = self.sample
        
        self.initialize_commands()
        
    def initialize_commands(self):
        for key, command in self.commands.items():
            if key in self.view.buttons.keys():
                self.view.buttons[key].configure(command=command)
        
    def sample(self):
        print("Sample")
        
    def update(self):
        self.view.update()