import numpy as np
from controls.Verifocal import Focuser

class Manager():
    def __init__(self):
        self.focuser = Focuser(1)
        self.focuser.reset(Focuser.OPT_ZOOM)
        self.focuser.reset(Focuser.OPT_FOCUS)
        self.action_space = (4)
        self.state_space = (18000, 18000)
        self.observation_space = (3, 256, 256)
    
    def choose_action(self):
        return np.random.randint(4)
    
    def move(self, cmd):
        self.focuser.move(cmd)
