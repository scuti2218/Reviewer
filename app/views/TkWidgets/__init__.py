from tkinter import Widget, Tk, Canvas, font as tkfont
from typing import Type
from abc import abstractmethod

# TkObject =============================================================
class TkObject:
    def __init__(self, **kwargs):
        self.init(**kwargs)
        self.post_update()
        
    @abstractmethod
    def init(self, **kwargs):
        pass
    
    def post_update(self):
        pass
    
    def get(self, key: str):
        return self.__dict__.get(key, "")
    
    def set(self, **kwargs):
        for key, value in kwargs:
            if value == None or key not in self.__dict__.keys(): continue
            self.__setattr__(key, value)
        self.post_update()

# TkColor =============================================================
class TkColor(TkObject):
    def init(self, **kwargs):
        self.normal: str = kwargs.get("normal", "#efefef")
        self.hover: str = kwargs.get("hover", "#c0c0c0")
        self.active: str = kwargs.get("active", "#111111")
            
# TkOutline =============================================================
class TkOutline(TkObject):
    def init(self, **kwargs):
        self.color: TkColor = TkColor( normal = kwargs.get("color_normal", "#111111"),
                                       hover = kwargs.get("color_hover", "#111111"),
                                       active = kwargs.get("color_active", "#111111") )
        self.width: int = kwargs.get("width", 0)
            
# TkOutline =============================================================
class TkDimension(TkObject):
    def init(self, **kwargs):
        self.width: int = kwargs.get("width", 0)
        self.height: int = kwargs.get("height", 0)
        self.radius: int = kwargs.get("radius", 0)
        self.outline: int = kwargs.get("outline", 0)
        self.post_update()
        
    def post_update(self):
        self.twidth: int = self.width + 2 * self.outline
        self.theight: int = self.height + 2 * self.outline

# RoundButton =============================================================
class RoundButton(Canvas):
    def __init__(self, parent, **kwargs):
        # Defaults
        groups = ["color", "font", "outline"]
        defaults = {grp:{} for grp in groups }
        for key, value in kwargs.items():
            if any([key.startswith(grp+"_") for grp in groups]):
                div = key.index("_")
                grp = key[:div]
                attr = key[div+1:]
                defaults[grp][attr] = value
        
        self.text = kwargs.get('text', '')
        self.font: tkfont.Font = tkfont.Font( **defaults["font"] )
        self.color: TkColor = TkColor( **defaults["color"] )
        self.outline = TkOutline( **defaults["outline"] )
        self.dimension = TkDimension(
            width = kwargs.get('width', self.font.measure(self.text) + 20),
            height = kwargs.get('height', self.font.metrics('linespace') + 10),
            radius = max(0, min(kwargs.get('radius', 1), 1.5 * self.outline.width)),
            outline = kwargs.get('outline', 0)
        )
        self.command = kwargs.get('command', lambda *_: "")
        
        # WIDGET INITIALIZATION
        super().__init__(parent, bg=parent['bg'], highlightthickness=0, width=self.dimension.twidth, height=self.dimension.theight, cursor="hand2")
        
        self.face_normal = lambda *_: self.create_face(self.color.normal, self.outline.color.normal)
        self.face_hover = lambda *_: self.create_face(self.color.hover, self.outline.color.hover)
        self.face_pressed = lambda *_: self.create_face(self.color.active, self.outline.color.active)
        self.init_events()
        
        self.face_normal()
    
    def init_events(self):
        self.bind('<Button-1>', self.on_click)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Enter>', self.face_hover)
        self.bind('<Leave>', self.face_normal)

    def on_click(self, event):
        self.face_pressed()
        
    def on_release(self, event):
        self.face_hover()
        self.command()
        
    def configure(self, **kwargs):
        if "command" in kwargs.keys():
            self.command = kwargs["command"]
            self.init_events()
            kwargs.pop("command")
        self.config(**kwargs)
        
    def create_face(self, color: str, outline: str, adjustment: TkDimension = TkDimension()):
        s = (self.dimension.twidth - adjustment.twidth, self.dimension.theight - adjustment.theight)
        r = self.dimension.radius
        w = self.outline.width
        
        self.config(width=s[0], height=s[1])
        self.delete('all')
        self.draw_face((0, 0), (s[0], s[1]), r, outline)
        self.draw_face((w, w), (s[0] - w, s[1] - w), r/3, color)
        self.create_text(s[0]/2, s[1]/2, text=self.text, font=self.font)
        
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

# TkWidget ============================================================
TWidget = Type[Widget]
class TkWidget:
    def __init__(self, widget_class: TWidget, root: Tk, **kwargs):
        self.value: TWidget = widget_class(root, **kwargs)
    
    def show(self, *args, **kwargs):
        self.value.pack(*args, **kwargs)
        
    def configure(self, **kwargs):
        self.value.configure(**kwargs)
        
# TkButton =============================================================
TTkWidget = Type[TWidget]
class TkButton(TkWidget):
    def __init__(self, root: Tk, **kwargs):
        super().__init__(RoundButton, root, **kwargs)
        
# class TkButton(TkWidget[Button]):
#     def __init__(self, root, key, **kwargs):
#         kwargs["text"] = key
#         super().__init__(Button, root, key, **kwargs)
        