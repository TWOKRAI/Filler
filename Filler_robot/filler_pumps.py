from pumps import Pump


class Motor:
    def __init__(self): 
        self.pump1 = Pump()
        self.pump1.motor = Motor(27, 22)

        self.pump2 = Pump()
        self.pump2.motor = Motor(18, 23)
	
	
    def all_pour(self):
        d1 = 0 
        d2 = 0
        
        turn1 = self.pump1.ml_to_step()
        turn2 = self.pump2.ml_to_step()
        
         
        
        while True:
            self.pump1.move(multi, turn1, self.pump1.direction)    
                
                
            if d1 <= turn1:
                d1 += 1
                self.pump1.motor.move(2, 1, self.pump1.direction)
            else:
                self.pump1.ready = True
                
            if d2 <= turn2:
                d2 += 1
                self.pump2.motor.move(2, 1, self.pump2.direction)
            else:
                self.pump2.ready = True
                
            #print('pump1', turn1, d1, self.pump2.motor.speed)
            #print('pump2', turn2, d2, self.pump2.motor.speed)
            
            if self.pump1.ready == True and self.pump2.ready == True:
                break
