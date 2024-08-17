from Raspberry.pins_table import pins
from PyQt5.QtCore import QThread
		

class Laser:
    def __init__(self) -> None:
        self.laser_on = False
        self.freq = 10
        self.i = False


    def running(self): 
        self.i += 1

        if self.i >= self.freq:
            self.laser_on_off()
            self.i = 0 
        

    def on_off(self, value):  
        pins.laser.set_value(value)

    
    def freq_func(self, frequ, coll):
        step = int(frequ/coll)

        for _ in range(coll):
            QThread.msleep(frequ)
            pins.laser.set_value(1)
            
            QThread.msleep(frequ)
            pins.laser.set_value(0)

            frequ -= step 
        
        self.on_off(1)



