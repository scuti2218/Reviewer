from services import ExecutionOrder
import tkinter as tk
from .TkWidgets import TkButton, TTkWidget, TvarTkObject, TkGroup, TkRadioGroup

class View(ExecutionOrder):
    # DEFAULT METHODS ====================================
    widget_types: list[TTkWidget] = [TkButton, TkGroup]
    root = tk.Tk()
    @staticmethod
    def get_widget_by_id(id: str):
        for widget in View.widget_types:
            if widget(View.root).widget_id == id:
                return widget
        return None
        
    def __init__(self):
        super().__init__()
        for widget in self.widget_types:
            self.__setattr__(f"create_{widget(self.root).widget_id}", lambda parent, key, **kwargs: self.create_widget(widget, parent, key, **kwargs))
        
        # widgets: dict[key, TTkWidget]
        self.widgets: dict[str, TTkWidget] = {}
        # objects: dict[key, TvarTkObject]
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
        ttkwidget = View.get_widget_by_id(id)
        if not ttkwidget: return
        self.templates[name] = (ttkwidget, kwargs)
        
    def create_radio_group(self, key: str):
        self.objects[f"rdgrp_{key}"] = TkRadioGroup()
        return self.objects[f"rdgrp_{key}"]
        
    def create_by_template(self, name: str, parent: tk.Tk, key: str, **kwargs):
        if name not in self.templates.keys(): return
        if key in self.widgets.keys(): return
        kwargs = self.templates[name][1] | kwargs
        return self.create_widget(self.templates[name][0], parent, key, **kwargs)
        
    def create_widget(self, widget: TTkWidget, parent: tk.Tk, key: str, **kwargs):
        if key in self.widgets.keys(): return
        self.widgets[key] = widget(parent, **kwargs)
        return self.widgets[key]
        
    # def create_button(self, parent, key: str, **kwargs):
    #     if key in self.widgets.keys(): return False
    #     self.widgets[key] = TkButton(parent, **kwargs)
        
    # def create_group(self, parent, key: str, **kwargs):
    #     if key in self.widgets.keys(): return False
    #     self.widgets[key] = TkGroup(parent, **kwargs)
        
    # UPDATE METHODS ====================================
    def update_buttons(self):
        for ttkwidget in self.widgets.values():
            ttkwidget.show()