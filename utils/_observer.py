import threading
from pyautogui import sleep

class Observer():
    def __init__(self, hook=None, rod=None, interval=.01) -> None:
        self.hook = hook
        self.rod = rod
        self.interval = interval
        self._built = None
        self._running = False
        return
    
    def _build_f(self):
        while(self._running):
            if(self.hook()):
                self.rod()
            sleep(self.interval)

    def _build_t(self):
        self._built = threading.Thread(target=self._build_f)
        return self._built
    
    @property
    def running(self):
        # Read-only hook for _running
        return self._running
    
    def start(self):
        self._running = True
        if (self._built is None):
            self._build_t()
        self._built.start()
        return
    
    def end(self):
        if not self._running:
            return
        self._terminate()
        self._running = False
    
    def _terminate(self):
        self._running = False