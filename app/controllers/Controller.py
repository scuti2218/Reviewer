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
        self.view.create_template("btn", "btn1", width=180, height=200, radius=25, outline_width=10)
        self.view.create_template("grp", "grp1")
        
        self.grp_modes = self.view.create_by_template("grp1", self.view.root, "grp_modes")
        
        rdgrp1 = self.view.create_radio_group('rdgrp1')
        self.view.create_by_template("btn1", self.grp_modes.value, "mode1", text="Tournament", command=self.cmd_btn_sample1, radio_group=rdgrp1, pack_side="left", margin_x=20)
        self.view.create_by_template("btn1", self.grp_modes.value, "mode2", text="Quiz", command=self.cmd_btn_sample2, radio_group=rdgrp1, pack_side="left", margin_x=20)
        self.view.create_by_template("btn1", self.grp_modes.value, "mode3", text="Flashcard", command=self.cmd_btn_sample3, radio_group=rdgrp1, pack_side="right")
        self.view.create_by_template("btn1", self.view.root, "mode4", text="CHECKBOX", command=self.cmd_btn_sample4, checkbox=True)
        
    def cmd_btn_sample1(self, *args):
        print("sample1")
    def cmd_btn_sample2(self, *args):
        print("sample2")
    def cmd_btn_sample3(self, *args):
        print("sample3")
    def cmd_btn_sample4(self, *args):
        print("sample4")