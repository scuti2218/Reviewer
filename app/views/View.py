from services import ExecutionOrder
import tkinter as tk
from .TkWidgets import TkButton

class View(ExecutionOrder):
    # DEFAULT METHODS ====================================
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.buttons: dict[str, TkButton] = {}
        
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
    def btn_create(self, key: str, **kwargs):
        self.buttons[key] = TkButton(self.root, key, **kwargs)
        
    # UPDATE METHODS ====================================
    def update_buttons(self):
        for tk_button in self.buttons.values():
            if tk_button.active:
                tk_button.show()