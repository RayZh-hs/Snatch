import pyautogui
from utils._observer import Observer

class Frame():
    def __init__(
                self, x=0, y=0, w=0, h=0,
                use_update=False, update_when=None, update_then=None, update_watch_internval=.01,
                use_tree=False, parent=None, children=[],
                ) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.use_update = use_update
        self.update_when = update_when
        self.update_then = update_then
        self.use_tree = use_tree
        self.parent = parent
        self.children = children
        self.inherit_update = True
        return
        
    def mid(self):
        return Frame(x=self.x+.5*self.w, y=self.y+.5*self.h)
    
    def left(self):
        return self.x
    
    def right(self):
        return self.x+self.w
    
    def top(self):
        return self.y
    
    def bottom(self):
        return self.y+self.h
    
    def size(self):
        return self.w*self.h
    
    def ispoint(self):
        return self.size() == 0

    def sub(
            self, x_offset=0, y_offset=0, x_scale=1, y_scale=1,
            w_offset=0, h_offset=0, w_scale=1, h_scale=1,
            use_default_update=True,
            parent_to_self=False,
            ):
        def _update(newself: Frame):
            par = newself.parent
            if par is None:
                return
            newself.x = par.x*x_scale+x_offset
            newself.y = par.y*y_scale+y_offset
            newself.w = par.w*w_scale+w_offset
            newself.h = par.h*h_scale+h_offset
            return newself
        new = Frame(
            x=self.x*x_scale+x_offset, y=self.y*y_scale+y_offset,
            w=self.w*w_scale+w_offset, h=self.h*h_scale+h_offset, 
            inherit_update=True,
        )
        if use_default_update:
            self.use_update = True
            self.update_when = lambda: False # only when parent updates
            self.update_then = _update
        if parent_to_self:
            new.parent = self
            self.children.append(new)
        return new

    def update(self):
        if self.use_update:
            if self.update_when():
                self.update_then(self)
        if self.use_tree:
            for child in self.children:
                child.update()
        return
    
    def start_update_cycle(self):
        self._observer = Observer(
            hook=self.update_when, rod=self.update_then, interval=self.update_watch_internval
        )
        self._observer.start()
        return

    def get(self):
        # get snapshot within frame
        return pyautogui.screenshot(region=(self.x, self.y, self.w, self.h))
