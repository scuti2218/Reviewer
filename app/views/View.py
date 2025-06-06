from services import ExecutionOrder
import tkinter as tk
from .TkWidgets import TkButton, TTkWidget, TvarTkObject, TkGroup, TkRadioGroup

class View(ExecutionOrder):
    # DEFAULT METHODS ====================================
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        # templates: dict[id, TTkWidget]
        self.widget_types: dict[str, TTkWidget] = {
            "btn" : TkButton,
            "grp" : TkGroup
        }
        # templates: dict[key, TTkWidget]
        self.widgets: dict[str, TTkWidget] = {}
        self.objects: dict[str, TvarTkObject] = {}
        # templates: dict[name, tuple[TTkWidget, kwargs]]
        self.templates: dict[str, tuple[TTkWidget, dict]] = {}
        
    def initialize(self):
        super().initialize()
        
    def preupdate(self):
        super().preupdate()
        self.root.title("Tkinter Fullscreen Centered Window")
        self.root.update_idletasks()
        self.init_window()
        
    def update(self):
        super().update()
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        label = tk.Label(frame, text="Hello, World!")
        label.pack()
        
    def postupdate(self):
        super().postupdate()
        self.update_buttons()
        self.root.mainloop()
        
    # CUSTOM METHODS ====================================
    def init_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.screen = (screen_width, screen_height)
        
        window_width = 800
        window_height = 600
        self.window = (window_width, window_height)
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.position = (x, y)
        
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.root.overrideredirect(False)
        
    # CREATE METHODS ====================================
    def create_template(self, id: str, name: str, **kwargs):
        if id not in self.widget_types.keys(): return
        ttkwidget: TTkWidget = self.widget_types[id]
        self.templates[name] = (ttkwidget, kwargs)
        
    def create_radio_group(self, key: str):
        self.objects[f"rdgrp_{key}"] = TkRadioGroup()
        return self.objects[f"rdgrp_{key}"]
        
    def create_by_template(self, parent, name: str, key: str, **kwargs):
        if name not in self.templates.keys(): return False
        if key in self.widgets.keys(): return False
        kwargs = self.templates[name][1] | kwargs
        self.create_widget(self.templates[name][0], parent, key, **kwargs)
        
    def create_widget(self, widget: TTkWidget, parent, key: str, **kwargs):
        if key in self.widgets.keys(): return False
        self.widgets[key] = widget(parent, **kwargs)
        
    def create_button(self, parent, key: str, **kwargs):
        if key in self.widgets.keys(): return False
        self.widgets[key] = TkButton(parent, **kwargs)
        
    def create_group(self, parent, key: str, **kwargs):
        if key in self.widgets.keys(): return False
        self.widgets[key] = TkGroup(parent, **kwargs)
        
    # UPDATE METHODS ====================================
    def update_buttons(self):
        for ttkwidget in self.widgets.values():
            ttkwidget.show()