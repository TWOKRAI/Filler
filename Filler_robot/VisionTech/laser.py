from Raspberry.pins_table import pins
from PyQt5.QtCore import QThread
		

class Laser:
    def __init__(self) -> None:
        self.mode = 1
        self.laser_on = False

        self.first = False

        self.freq = 100
        self.coll = 20
        self.step = 10


    def running(self):
        if self.first:
            self.on_off(1)
            QThread.msleep(2100)

        match self.mode:
            case 0:
                self.on_off(0)
            case 1:
                self.on_off(1)
            case 2:
                self.freq_func(self.freq, self.coll, self.step)
            case _:
                self.on_off(0)

        self.first = True
        

    def on_off(self, value):
        if  self.mode != 0:
            pins.laser.set_value(value)
        else:
            pins.laser.set_value(0)

    
    def freq_func(self, frequ, coll, step):
        for _ in range(coll):
            QThread.msleep(frequ)
            pins.laser.set_value(1)
            
            QThread.msleep(frequ)
            pins.laser.set_value(0)

            frequ -= step 

            if frequ <= 0:
                frequ = 1
        
        self.on_off(0)



