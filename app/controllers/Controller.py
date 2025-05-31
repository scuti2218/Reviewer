from views import View
from models import Model

class Controller:
    # CONSTANT METHODS ====================================
    def __init__(self):
        self.view = View()
        self.model = Model()
        self.initialize()
        
    def initialize(self):
        self.view.initialize()
        self.model.initialize()
        self.init_controller()
        
    def update(self):
        self.model.preupdate()
        self.view.preupdate()
        
        self.model.update()
        self.view.update()
        
        self.model.postupdate()
        self.view.postupdate()
        
    # DEFAULT METHODS ====================================
    def init_controller(self):
        self.view.btn_create("sample", text="TRIALLSSS", width=180, height=70, outline_thickness=10, radius=25)
        self.init_commands()
        
    # CUSTOM METHODS ====================================
    def init_commands(self):
        commands = { name[4:]:getattr(self, name)
                    for name in dir(self)
                    if name.startswith('cmd_')
                    and callable(getattr(self, name)) }
        for key, command in commands.items():
            if key in self.view.buttons.keys():
                self.view.buttons[key].configure(command=lambda *args: command(self, *args))
    
    def cmd_sample(self, *args):
        print("sample")