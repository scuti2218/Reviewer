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
        self.view.create_template("btn", "btn1", width=180, height=70, radius=25, outline_width=10)
        
        self.view.create_by_template("btn1", "btn_sample", text="This button", command=self.cmd_btn_sample)
        # self.view.create_button("btn_sample2", text="TRIALLSSS", width=180, height=70, outline_thickness=10, radius=25)
        
        print(self.view.widgets)
        
    def cmd_btn_sample(self, *args):
        print("sample")
    def cmd_btn_sample2(self, *args):
        print("heeyyyy")