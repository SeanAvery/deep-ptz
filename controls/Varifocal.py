import sys
import time
class Focuser:
    bus = None
    CHIP_I2C_ADDR = 0x0C
    BUSY_REG_ADDR = 0x04
    starting_point = [
        11000, 10000, 10000, 
        10000, 10000, 9800, 
        9600, 9000, 8500, 
        8000, 7000, 6000, 
        5000, 3500, 2000, 
        0, 0, 0, 0
    ]
    end_point = [
        18000, 18000, 18000, 
        18000, 18000, 18000, 
        18000, 17500, 17500, 
        16500, 16000, 15000, 
        14000, 12500, 11000, 
        9500, 7500, 5000, 4000
    ]
    def __init__(self,bus):
        try:
            import smbus
            self.bus = smbus.SMBus(bus)
        except:
            sys.exit(0)
        
    def read(self,chip_addr,reg_addr):
        value = self.bus.read_word_data(chip_addr,reg_addr)
        value = ((value & 0x00FF)<< 8) | ((value & 0xFF00) >> 8)
        return value
    def write(self,chip_addr,reg_addr,value):
        if value < 0:
            value = 0
        value = ((value & 0x00FF)<< 8) | ((value & 0xFF00) >> 8)
        return self.bus.write_word_data(chip_addr,reg_addr,value)
    def isBusy(self):
        return self.read(self.CHIP_I2C_ADDR,self.BUSY_REG_ADDR) != 0
    def waitingForFree(self):
        count = 0
        begin = time.time()
        while self.isBusy() and count < (5 / 0.01):
            count += 1
            time.sleep(0.01)
        # if count >= (5 / 0.01):
        #     print "wait timeout."
        # elif count != 0:
        #     print "wait time = %lf"%(time.time() - begin)

    OPT_BASE    = 0x1000
    OPT_FOCUS   = OPT_BASE | 0x01
    OPT_ZOOM    = OPT_BASE | 0x02
    OPT_MOTOR_X = OPT_BASE | 0x03
    OPT_MOTOR_Y = OPT_BASE | 0x04
    OPT_IRCUT   = OPT_BASE | 0x05
    opts = {
        OPT_FOCUS : {
            "REG_ADDR" : 0x01,
            "MAX_VALUE": 18000,
            "RESET_ADDR": 0x01 + 0x0A,
        },
        OPT_ZOOM  : {
            "REG_ADDR" : 0x00,
            "MAX_VALUE": 18000,
            "RESET_ADDR": 0x00 + 0x0A,
        },
        OPT_MOTOR_X : {
            "REG_ADDR" : 0x05,
            "MAX_VALUE": 180,
            "RESET_ADDR": None,
        },
        OPT_MOTOR_Y : {
            "REG_ADDR" : 0x06,
            "MAX_VALUE": 180,
            "RESET_ADDR": None,
        },
        OPT_IRCUT : {
            "REG_ADDR" : 0x0C, 
            "MAX_VALUE": 0x01,   #0x0001 open, 0x0000 close
            "RESET_ADDR": None,
        }
    }
    def reset(self,opt,flag = 1):
        self.waitingForFree()
        info = self.opts[opt]
        if info == None or info["RESET_ADDR"] == None:
            return
        self.write(self.CHIP_I2C_ADDR,info["RESET_ADDR"],0x0000)
        if flag & 0x01 != 0:
            self.waitingForFree()

    def get(self,opt,flag = 0):
        self.waitingForFree()
        info = self.opts[opt]
        return self.read(self.CHIP_I2C_ADDR,info["REG_ADDR"])

    def set(self,opt,value,flag = 1):
        self.waitingForFree()
        info = self.opts[opt]
        if value > info["MAX_VALUE"]:
            value = info["MAX_VALUE"]
        self.write(self.CHIP_I2C_ADDR,info["REG_ADDR"],value)
        if flag & 0x01 != 0:
            self.waitingForFree()
    def move(self, cmd, counter):
        print('hit move:', cmd)
        # zoom in
        val = 0
        if cmd == 0:
            val = self.get(self.OPT_ZOOM) + counter
            if val > 18000:
                val = 18000
            print('val', val)
            self.set(self.OPT_ZOOM, val)
        # zoom out
        if cmd == 1:
            val = self.get(self.OPT_ZOOM) - counter
            if val < 0:
                val = 0
            self.set(self.OPT_ZOOM, val)
        # focus in
        if cmd == 2:
            val = self.get(self.OPT_FOCUS) + counter
            if val > 18000:
                val = 18000
            self.set(self.OPT_FOCUS, val)
        # focus out
        if cmd == 3:
            val = self.get(self.OPT_FOCUS) - counter
            if val < 0:
                val = 0
            self.set(self.OPT_FOCUS, val)
        print('val', val)

pass 


def test():
    focuser = Focuser(1)
    focuser.reset(Focuser.OPT_FOCUS)
    focuser.reset(Focuser.OPT_ZOOM)
    # sys.exit(0)
    # while focuser.get(Focuser.OPT_FOCUS) < 18000:
    #     focuser.set(Focuser.OPT_FOCUS,focuser.get(Focuser.OPT_FOCUS) + 50)
    # focuser.set(Focuser.OPT_FOCUS,0)
    # focuser.set(Focuser.OPT_FOCUS, 12000)
    # focuser.set(Focuser.OPT_ZOOM, 12000)
    import random
    import time
    while True:
        focuser.move(random.randint(0, 3))

pass

if __name__ == "__main__":
    test()
