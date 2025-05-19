from tkinter import Widget, Tk, Button
from typing import Generic, TypeVar, Type

# TkWidget =============================================================
TWidget = TypeVar('TWidget', bound=Widget)
class TkWidget(Generic[TWidget]):
    def __init__(self, widget_class: Type[TWidget], root: Tk, key: str, **kwargs):
        self.active = True
        self.key = key
        self.value: TWidget = widget_class(root, **kwargs)
    
    def toggle(self):
        self.active = not self.active
        
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False
        
    def set_activate(self, active: bool):
        self.active = active
    
    def show(self, *args, **kwargs):
        self.value.pack(*args, **kwargs)
        
    def configure(self, **kwargs):
        self.value.configure(**kwargs)

# TkButton =============================================================
class TkButton(TkWidget[Button]):
    def __init__(self, root, key, **kwargs):
        super().__init__(Button, root, key, **kwargs)