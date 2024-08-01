from PyQt5.QtCore import QThread
import asyncio

from Filler_robot.MotorModules.motor import Motor
from Raspberry.pins_table import pins


class Motor_monitor(QThread):
    def __init__(self):
        super().__init__()

        self.state = False

        self.motor = Motor('motor-monitor', pins.motor_step, pins.motor_dir, pins.motor_enable)

        self.motor.direction = False

        self.motor.acc_run = True
        self.motor.k = 10
        self.acc_start = 20
        self.acc_end = 20
        
        self.motor.speed_def = 0.00001
        
        self.motor.limit_min = -19100
        self.motor.limit_max = 19100
        self.distance = 19000

        self.direction = True

        self.state_button = False
        self.not_button = False

        self.motor.enable_on(True)


    def run(self):
        self.running = True 
        
        switch_out = pins.switch_out.get_value()
        switch_in = pins.switch_in.get_value()

        self.motor.enable_on(False)
        self.motor.null_value()

        if switch_in == True:
            distance = -self.distance

        elif switch_out == True:
            distance = self.distance

        elif switch_in == False and switch_out == False:
            if self.state_button:
                distance = self.distance
            else:
                distance = -self.distance

        asyncio.run(self._move_async(distance, detect = True))
        self.direction = not self.direction
        

    async def _detect_sensor(self):
        while True:
            dir = pins.motor_dir.get_value()
            switch_out = pins.switch_out.get_value()
            switch_in = pins.switch_in.get_value()
            button = pins.button.get_value()

            if not button:
                self.not_button = True

            if button and self.not_button:
                self.state_button = not self.state_button
                self.not_button = False
                raise asyncio.CancelledError()
            
            if self.motor.ready:
                raise asyncio.CancelledError()

            if (switch_in and not dir) or (switch_out and dir):
                print('SWITCH')
                self.state = not self.state
                raise asyncio.CancelledError()

            await asyncio.sleep(0.001)


    async def _move_async(self, distance, detect = False):
        tasks = []

        if detect:
            tasks.append(asyncio.create_task(self._detect_sensor()))

        tasks.append(asyncio.create_task(self.motor._freq_async(2000, 1, distance)))
            
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()
                
        print('ready')
        self.motor.enable_on(True)
        self.motor.ready = False


motor_monitor = Motor_monitor()


if __name__ == '__main__':
    while True:
        motor_monitor.run()