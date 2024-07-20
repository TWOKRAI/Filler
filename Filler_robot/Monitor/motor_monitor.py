from PyQt5.QtCore import QThread, pyqtSignal
import asyncio

from Gadgets.MotorModules.motor import Motor
from Raspberry.pins_table import pins


class Motor_monitor(QThread):
    def __init__(self):
        self.pin_motor_step = 15
        self.pin_motor_dir = 21
        self.pin_motor_enable = 16

        self.pin_button = 7
        self.pin_switch_out = 8
        self.pin_switch_in = 6

        self.motor = Motor('motor-monitor', pins.motor_step, pins.motor_dir, pins.motor_enable)
        
        self.motor.acc_run = True
        self.motor.k = 10
        self.acc_start = 30
        self.acc_end = 30
        
        self.motor.speed_def = 0.00001
        
        self.motor.limit_min = -19100
        self.motor.limit_max = 19100
        self.distance = 19000

        self.direction = True

        self.state = False
        self.not_button = False

        self.motor.enable_on(True)


    def run(self):
        button = pins.get_value(pins.button)
        switch_out = pins.get_value(pins.switch_out)
        switch_in = pins.get_value(pins.switch_in)

        if button == True and switch_in == True:
            self.motor.enable_on(False)
            self.motor.null_value()

            distance = -self.distance
            asyncio.run(self._move_async(distance, detect = True))
            self.direction = not self.direction

        elif button == True and switch_out == True:
            self.motor.enable_on(False)
            self.motor.null_value()

            distance = self.distance
            asyncio.run(self._move_async(distance, detect = True))
            self.direction = not self.direction

        elif button == True and switch_in == False and switch_out == False:
            self.motor.enable_on(False)
            self.motor.null_value()

            if self.state:
                distance = self.distance
            else:
                distance = -self.distance

            asyncio.run(self._move_async(distance, detect = True))
            self.direction = not self.direction

        # if self.motor.distance_step >= 25 and len(self.motor.data) != 0:
        #     plotter = Plotter(self.motor.data, self.motor.distance_step)
        #     plotter.plot()

        #     self.motor.data = []
        #     self.motor.distance_step = 0


    async def _detect_sensor(self):
        while True:
            dir = pins.get_value(pins.motor_dir)
            switch_out = pins.get_value(pins.switch_out)
            switch_in = pins.get_value(pins.switch_in)
            button = pins.get_value(pins.button)

            if not button:
                self.not_button = True

            if button and self.not_button:
                self.state = not self.state
                self.not_button = False
                raise asyncio.CancelledError()
            
            if self.motor.ready:
                raise asyncio.CancelledError()

            if (switch_in and dir) or (switch_out and not dir):
                self.motor.enable_on(True)
                print('SWITCH')
                raise asyncio.CancelledError()

            await asyncio.sleep(0.05)


    async def _move_async(self, distance, detect = False):
        tasks = []

        if detect:
            tasks.append(asyncio.create_task(self._detect_sensor()))

        tasks.append(asyncio.create_task(self.motor.move(distance, async_mode=True)))
            
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()
                
        print('ready')
        self.motor.ready = False


motor_monitor = Motor_monitor()


while True:
    motor_monitor.run()
    
