from tkinter import Widget, Tk, Button, Canvas, font as tkfont
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
        
class RoundButton(Canvas):
    def __init__(self, parent, **kwargs):
        # Defaults
        font = kwargs.get('font', 10)
        text = kwargs.get('text', '')
        obj_font = tkfont.Font(size = font)
        width = kwargs.get('width', obj_font.measure(text) + 20)
        height = kwargs.get('height', obj_font.metrics('linespace') + 10)
        command = kwargs.get('command', lambda *_: "")
        color = kwargs.get('color', '#ffffff')
        hover = kwargs.get('hover', "#e8e8e8")
        zoom = kwargs.get('zoom', 5)
        outline = kwargs.get('outline', '#000000')
        outline_thickness = kwargs.get('outline_thickness', 2)
        radius = kwargs.get('radius', 1)
        radius = max(0, min(radius, 1.5 * outline_thickness))
        
        # WIDGET INITIALIZATION
        total_width = width + 2 * outline_thickness
        total_height = height + 2 * outline_thickness
        super().__init__(parent, bg=parent['bg'], highlightthickness=0, width=total_width, height=total_height)
        self.create_face((total_width, total_height), radius, outline_thickness, outline, color, text, font)
        
        # MODIFICATION
        self.bind('<Button-1>', lambda _: command)
        self.bind('<Enter>', lambda e: self.create_face((total_width, total_height), radius, outline_thickness, outline, hover, text, font, zoom))
        self.bind('<Leave>', lambda e: self.create_face((total_width, total_height), radius, outline_thickness, outline, color, text, font))
        
    def configure(self, **kwargs):
        if "command" in kwargs.keys():
            self.bind('<Button-1>', kwargs["command"])
            kwargs.pop("command")
        self.config(**kwargs)
        
    def create_face(self, s: tuple[int, int], r, w, outline, color, text, font: int, adjustment: int = 0):
        s = (s[0]+adjustment, s[1]+adjustment)
        # font = max(1, int(min(s[1] * 0.5, s[0] / 6)))
        
        self.config(width=s[0], height=s[1])
        self.delete('all')
        self.draw_face((0, 0), (s[0], s[1]), r, outline)
        self.draw_face((w, w), (s[0] - w, s[1] - w), r/3, color)
        self.create_text(s[0]/2, s[1]/2, text=text, font=tkfont.Font(size = font))
        
    def draw_face(self, a: tuple[int, int], b: tuple[int, int], width, color):
        x1, y1 = a
        x4, y4 = b
        
        x2 = x1 + width
        x3 = x4 - width
        
        y2 = y1 + width
        y3 = y4 - width
        
        # OUTLINE CORNERS
        xt = width
        self.create_arc(x1, y1, x2+xt, y2+xt, start=90, extent=90, fill=color, width=0)  # UL      
        self.create_arc(x3-xt, y1, x4, y2+xt, start=0, extent=90, fill=color, width=0)   # UR   
        self.create_arc(x1, y3-xt, x2+xt, y4, start=180, extent=90, fill=color, width=0) # BL      
        self.create_arc(x3-xt, y3-xt, x4, y4, start=270, extent=90, fill=color, width=0) # BR
        
        # OUTLINE EDGES
        xt = 1 # Extra thickness
        self.create_rectangle(x1, y2-xt, x2, y3+xt, fill=color, width=0) # L
        self.create_rectangle(x3, y2-xt, x4, y3+xt, fill=color, width=0) # R
        self.create_rectangle(x2-xt, y1, x3+xt, y2, fill=color, width=0) # U
        self.create_rectangle(x2-xt, y3, x3+xt, y4, fill=color, width=0) # B
        
        # OUTLINE MIDDLE
        xt = 0
        self.create_rectangle(x2-xt, y2-xt, x3+xt, y3+xt, fill=color, width=0) # vertical
    

# TkButton =============================================================
class TkButton(TkWidget[RoundButton]):
    def __init__(self, root, key, **kwargs):
        kwargs["text"] = kwargs.get("text", key)
        super().__init__(RoundButton, root, key, **kwargs)
        
# class TkButton(TkWidget[Button]):
#     def __init__(self, root, key, **kwargs):
#         kwargs["text"] = key
#         super().__init__(Button, root, key, **kwargs)
        