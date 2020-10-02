import numpy as np
from controls.Varifocal import Focuser

class Manager():
    def __init__(self):
        self.focuser = Focuser(1)
        # reset to (0, 0)
        self.focuser.reset(Focuser.OPT_ZOOM)
        self.focuser.reset(Focuser.OPT_FOCUS)
        # set to default (3000, 12000)
        self.focuser.set(Focuser.OPT_ZOOM, 3000)
        self.focuser.set(Focuser.OPT_FOCUS, 9000)
        
        # initialize state space
        self.action_space = (4)
        self.state_space = (18000, 18000)
        
        self.observation_space = (3, 256, 256)
        print('zoom:', self.focuser.get(Focuser.OPT_ZOOM))
        print('focus', self.focuser.get(Focuser.OPT_FOCUS))
        self.counter = 1

    def linear_decay(self, counter):
        val = int(1000 / (counter))
        if val < 10:
            return 10
        else:
            return val
    
    def choose_action(self):
        return np.random.randint(4)
    
    def move(self, cmd):
        self.focuser.move(cmd, self.linear_decay(self.counter))
        self.counter+=1
        
