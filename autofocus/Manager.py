import numpy as np
from controls.Varifocal import Focuser

class Manager():
    def __init__(self):
        self.focuser = Focuser(1)
        # what am i reset too
        self.focuser.reset(Focuser.OPT_ZOOM)
        self.focuser.reset(Focuser.OPT_FOCUS)
        self.focuser.set(Focuser.OPT_ZOOM, 3000)
        self.action_space = (4)
        self.state_space = (18000, 18000)
        self.observation_space = (3, 256, 256)
        print('zoom:', self.focuser.get(Focuser.OPT_ZOOM))
        print('focus', self.focuser.get(Focuser.OPT_FOCUS))
    
    def choose_action(self):
        return np.random.randint(4)
    
    def move(self, cmd):
        self.focuser.move(cmd)
