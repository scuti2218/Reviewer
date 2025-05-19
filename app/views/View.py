import tkinter as tk
from .TkWidgets import TkButton

class View:
    def __init__(self):
        self.root = tk.Tk()
        self.buttons: dict[str, TkButton] = {}
        
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
        
    def initialize(self):
        self.btn_create("sample", text='Stop', width=25)
        
    def update(self):
        self.root.title("Tkinter Fullscreen Centered Window")
        self.root.update_idletasks()
        self.init_window()
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        label = tk.Label(frame, text="Hello, World!")
        label.pack()
        
        self.update_buttons()
        print(self.buttons)
        self.root.mainloop()
        
    def update_buttons(self):
        for tk_button in self.buttons.values():
            if tk_button.active:
                tk_button.show()
        
    def btn_create(self, key: str, **kwargs):
        self.buttons[key] = TkButton(self.root, key, **kwargs)