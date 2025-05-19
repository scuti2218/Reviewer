from ..views import View
from ..models import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model
        self.initialize()
        
    def initialize(self):
        self.view.initialize()
        self.model.initialize()
        
        self.view.btn_create("sample", text='Stop', width=25)
        
    def update(self):
        self.view.update()