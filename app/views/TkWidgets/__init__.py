from tkinter import Widget, Tk, Canvas, font as tkfont
from typing import Type, TypeVar
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
TTkObject = Type[TkObject]
TvarTkObject = TypeVar("TkObject", bound=TkObject)

# TkColor =============================================================
class TkColor(TkObject):
    def init(self, **kwargs):
        self.normal: str = kwargs.get("normal", "#efefef")
        self.hover: str = kwargs.get("hover", "#c0c0c0")
        self.active: str = kwargs.get("active", "#4C4C4C")
        
    @staticmethod
    def get_contrasting_text_color(color: str):
        if color.startswith("#"):
            r, g, b = [int(color[i:i+2], 16) for i in (1, 3, 5)]
        else:
            import tkinter as tk
            t = tk.Tk()
            t.withdraw()
            r, g, b = [v // 256 for v in t.winfo_rgb(color)]
            t.destroy()
        return "black" if (0.299*r + 0.587*g + 0.114*b) > 186 else "white"
            
# TkOutline =============================================================
class TkOutline(TkObject):
    def init(self, **kwargs):
        self.color: TkColor = TkColor( normal = kwargs.get("color_normal", "#111111"),
                                       hover = kwargs.get("color_hover", "#111111"),
                                       active = kwargs.get("color_active", "#111111") )
        self.width: int = kwargs.get("width", 0)
            
# TkCommand =============================================================
class TkCommand(TkObject):
    def init(self, **kwargs):
        self.on_select: str = kwargs.get("on_select", TkCommand.get_default())
        self.on_enter: str = kwargs.get("on_enter", TkCommand.get_default())
        self.on_leave: str = kwargs.get("on_leave", TkCommand.get_default())
        self.on_click: str = kwargs.get("on_click", TkCommand.get_default())
        self.on_release: str = kwargs.get("on_release", TkCommand.get_default())
        
    @staticmethod
    def get_default():
        return lambda *_: ""
        
        
            
# TkOutline =============================================================
class TkDimension(TkObject):
    def init(self, **kwargs):
        self.width: int = kwargs.get("width", 0)
        self.height: int = kwargs.get("height", 0)
        self.radius: int = kwargs.get("radius", 0)
        self.outline: int = kwargs.get("outline", 0)
        self.padding_x: int = kwargs.get("padding_x", 0)
        self.padding_y: int = kwargs.get("padding_y", 0)
        self.margin_x: int = kwargs.get("margin_x", 0)
        self.margin_y: int = kwargs.get("margin_y", 0)
        self.post_update()
        
    def post_update(self):
        self.twidth: int = self.width + 2 * self.outline
        self.theight: int = self.height + 2 * self.outline

# ITkRadioGroupable =============================================================
class TkRadioGroupData:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', '')
        self.selected = False
        self.radio_group: TkRadioGroup = kwargs.get('radio_group', None)
        
    def on_radio_true(self):
        self.selected = True
    
    def on_radio_false(self):
        self.selected = False

# TkRadioGroup =============================================================
class TkRadioGroup(TkObject):
    def init(self, **_):
        self.contents: list[TkRadioGroupData] = []
        self.__curselected = ''
        
    def add(self, data: TkRadioGroupData):
        self.contents.append(data)
        
    def activate(self, id: str):
        for content in self.contents:
            if content.id == id:
                self.__deactivate(self.__curselected)
                self.__curselected = id
                content.on_radio_true()
                return
            
    def __deactivate(self, id):
        for content in self.contents:
            if content.id == id:
                content.on_radio_false()
                return
            

# TkCanvas =============================================================
class TkCanvas(Canvas):
    def get_kwargs(self, groups: list[str], kwargs: dict):
        defaults = {grp:{} for grp in groups }
        for key, value in kwargs.items():
            if any([key.startswith(grp+"_") for grp in groups]):
                div = key.index("_")
                grp = key[:div]
                attr = key[div+1:]
                defaults[grp][attr] = value
        return defaults
    
    def __init__(self, parent, **kwargs):
        # Defaults
        defaults = self.get_kwargs(["color", "font", "outline"], kwargs)
        self.children: list[TvarTkWidget] = kwargs.get("children", [])
        
        self.text = kwargs.get('text', '')
        self.font: tkfont.Font = tkfont.Font( **defaults["font"] )
        self.color: TkColor = TkColor( **defaults["color"] )
        self.outline = TkOutline( **defaults["outline"] )
        padding_x = 40
        padding_y = 40
        self.dimension = TkDimension(
            padding_x = kwargs.get('padding_x', padding_x),
            padding_y = kwargs.get('padding_y', padding_y),
            width = kwargs.get('width', self.font.measure(self.text) + padding_x),
            height = kwargs.get('height', self.font.metrics('linespace') + padding_y),
            radius = max(0, min(kwargs.get('radius', 1), 1.5 * self.outline.width)),
            outline = kwargs.get('outline', 0),
            margin_x = kwargs.get('margin_x', 0),
            margin_y = kwargs.get('margin_y', 0)
        )
        self.cursor = kwargs.get("cursor", "hand1")
        self.highlightthickness = kwargs.get("highlightthickness", 0)
        self.face_normal = lambda *_: self.__face_pressed()
        super().__init__(parent, bg=parent['bg'], width=self.dimension.twidth, height=self.dimension.theight, highlightthickness=self.highlightthickness, cursor=self.cursor)
        self.initialize(**kwargs)
        self.dimension_postprocess()
        
    def __face_pressed(self):
        self.font.config(weight='normal')
        self.create_face(self.color.normal, self.outline.color.normal)
    
    def dimension_postprocess(self):
        bbox = self.bbox("all")
        if bbox:
            self.configure(width=bbox[2] - 2 + self.dimension.margin_x, height=bbox[3] - 2 + self.dimension.margin_y)
        
    def initialize(self, **kwargs):
        pass
        
    def draw_face(self, a: tuple[int, int], b: tuple[int, int], width, color):
        x1, y1 = a
        x4, y4 = b
        
        x2 = x1 + width
        x3 = x4 - width
        
        y2 = y1 + width
        y3 = y4 - width
        
        # MIDDLE
        xt = 0
        self.create_rectangle(x2-xt, y2-xt, x3+xt, y3+xt, fill=color, width=0) # vertical
        
        # CORNERS
        xt = width
        self.create_arc(x1, y1, x2+xt, y2+xt, start=90, extent=90, fill=color, width=0)  # UL      
        self.create_arc(x3-xt, y1, x4, y2+xt, start=0, extent=90, fill=color, width=0)   # UR   
        self.create_arc(x1, y3-xt, x2+xt, y4, start=180, extent=90, fill=color, width=0) # BL      
        self.create_arc(x3-xt, y3-xt, x4, y4, start=270, extent=90, fill=color, width=0) # BR
        
        # EDGES
        xt = 1 # Extra thickness
        self.create_rectangle(x1, y2-xt, x2, y3+xt, fill=color, width=0) # L
        self.create_rectangle(x3, y2-xt, x4, y3+xt, fill=color, width=0) # R
        self.create_rectangle(x2-xt, y1, x3+xt, y2, fill=color, width=0) # U
        self.create_rectangle(x2-xt, y3, x3+xt, y4, fill=color, width=0) # B
        
    def create_face(self, color: str, outline: str, adjustment: TkDimension = TkDimension()):
        s = (self.dimension.twidth - adjustment.twidth, self.dimension.theight - adjustment.theight)
        r = self.dimension.radius
        w = self.outline.width
        
        self.delete('all')
        self.draw_face((0, 0), (s[0], s[1]), r, outline)
        self.draw_face((w, w), (s[0] - w, s[1] - w), r/3, color)
        self.create_text(s[0]/2, s[1]/2, text=self.text, font=self.font, fill=TkColor.get_contrasting_text_color(color))
        for child in self.children:
            self.create_window()
        self.config(width=s[0], height=s[1])
        self.dimension_postprocess()

# RoundButton =============================================================
class RoundButton(TkCanvas, TkRadioGroupData):
    registry = []
    def __init__(self, parent, **kwargs):
        # WIDGET INITIALIZATION
        id = f"rbtn{len(self.registry)}"
        TkRadioGroupData.__init__(self, id=id, **kwargs)
        TkCanvas.__init__(self, parent, cursor="hand2", **kwargs)
        RoundButton.registry.append(self)
    
    def initialize(self, **kwargs):
        if self.radio_group: self.radio_group.add(self)
        self.checkbox = [kwargs.get('checkbox', False), False][self.radio_group != None]
        
        if "command" in kwargs.keys():
            kwargs["command_on_select"] = kwargs["command"]
            kwargs.pop("command")
        defaults = self.get_kwargs(["command"], kwargs)
        self.command = TkCommand(**defaults["command"])
        
        self.face_hover = lambda *_: self.create_face(self.color.hover, self.outline.color.hover)
        self.face_pressed = lambda *_: self.__face_pressed()
        self.init_events()
        
        self.face_normal()
        
    def __face_pressed(self):
        self.font.config(weight='bold')
        self.create_face(self.color.active, self.outline.color.active)

    def init_events(self):
        self.bind('<Button-1>', self.on_click)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def on_radio_true(self):
        super().on_radio_true()
        self.face_pressed()
    
    def on_radio_false(self):
        super().on_radio_false()
        self.face_normal()

    def on_click(self, _):
        self.face_pressed()
        self.command.on_click()
        
    def on_release(self, _):
        if self.checkbox:
            self.selected = not self.selected
            if self.selected:
                self.face_pressed()
                self.command.on_select()
            else:
                self.face_hover()
        elif self.radio_group:
            if not self.selected:
                self.radio_group.activate(self.id)
                self.command.on_select()
        else:
            self.face_hover()
            self.command.on_select()
        self.command.on_release()
        
    def on_enter(self, _):
        if self.checkbox:
            if not self.selected:
                self.face_hover()
                self.command.on_enter()
        elif self.radio_group:
            if not self.selected:
                self.face_hover()
                self.command.on_enter()
        else:
            self.face_hover()
            self.command.on_enter()
        
    def on_leave(self, _):
        if self.checkbox:
            if not self.selected:
                self.face_normal()
                self.command.on_enter()
        elif self.radio_group:
            if not self.selected:
                self.face_normal()
                self.command.on_enter()
        else:
            self.face_normal()
            self.command.on_enter()

# TkWidget ============================================================
TWidget = Type[Widget]
class TkWidget:
    def __init__(self, widget_class: TWidget, widget_id: str, root: Tk, **kwargs):
        self.widget_id = widget_id
        groups = ["pack"]
        defaults = {grp:{} for grp in groups }
        pops = []
        for key, value in kwargs.items():
            if any([key.startswith(grp+"_") for grp in groups]):
                div = key.index("_")
                grp = key[:div]
                attr = key[div+1:]
                defaults[grp][attr] = value
                pops.append(key)
        for i in pops:
            kwargs.pop(i)
        self.pack = defaults["pack"]
        self.value: TWidget = widget_class(root, **kwargs)
    
    def show(self, *args, **kwargs):
        self.value.pack(*args, **self.pack, **kwargs)
        
    def configure(self, **kwargs):
        self.value.configure(**kwargs)
TTkWidget = Type[TkWidget]
TvarTkWidget = TypeVar("TkWidget", bound=TkWidget)
        
# TkButton =============================================================
class TkButton(TkWidget):
    def __init__(self, root: Tk, **kwargs):
        super().__init__(RoundButton, "btn", root, **kwargs)
        
# TkGroup =============================================================
class TkGroup(TkWidget):
    def __init__(self, root: Tk, **kwargs):
        super().__init__(TkCanvas, "grp", root, **kwargs)