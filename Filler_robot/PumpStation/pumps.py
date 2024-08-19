import asyncio
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from Filler_robot.MotorModules.motor import Motor
# from Filler_robot.NeuroModules.neuron import neuron

from Raspberry.pins_table import pins

from Filler_interface import app

from Filler_interface.filler import filler


class Pump(QObject):
    def __init__(self, name, motor):
        super().__init__()

        self.print_on = True

        self.name = name

        self.motor = motor
        
        self.turn = 0
        self.ml = 30
        self.amount = 1
        self.step_amount = 0.003
        self.speed = 10
        self.speed_k = 100

        self.dir = 1

        self.bottle_ml = 1000
        self.bottle_min = 100

        self.warnning = False
        self.ready = False
    

    def ml_to_steps(self, ml):
        steps = 0
        if ml >= 0:
            steps = int(ml) / self.step_amount
        else:
            steps = int(ml) / self.step_amount

        if self.print_on:
            print(self.ml, self.step_amount)
            print(f'pump {self.name}, ml_to_steps // output: steps = {steps} bottle {self.bottle_ml}')

        return steps
    

    def step_to_ml(self):
        return int(self.motor.value * self.amount / self.step_amount)


    async def _pour_async(self, ml):
        self.motor.stop = False
        self.ready = False
        
        self.turn = self.ml_to_steps(ml)

        speed = int(self.speed_k * self.speed)

        print('speed', self.speed_k, speed, self.turn)

        await self.motor._freq_async(speed, 1, self.turn)

        # QThread.sleep(1)
        
        # await self.motor._freq_async(speed, 1, 1000 * -self.dir)
        
        await self.motor._freq_async(speed, 1, -500 * self.dir, accuration = False)

        self.ready = True
        

    def pour(self, ml, async_mode: bool = False):
        self.motor.stop = False
        self.ready = False

        self.motor.value = 0
        self.motor.error_limit = False
        
        if async_mode:
            return self._pour_async(ml)
        else:
            asyncio.run(self._pour_async(ml))
    

    async def _pour_async_down(self, dir):
        self.motor.stop = False
        self.ready = False

        if dir == True:
            await self.motor._freq_async(10, 1, -500 * self.dir, accuration = False)
        else:
            await self.motor._freq_async(10, 1, -500 * self.dir, accuration = False)
    

class Pump_station(QObject):
    minus_pump = pyqtSignal()
    bottle_1 = pyqtSignal()
    bottle_2 = pyqtSignal()
    start_pump = pyqtSignal()
    stop_pump = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self.running = True

        self.motor_1 = Motor('pumps_1', pins.motor_p1_step, pins.motor_p1_dir, pins.motor_p1p2_enable)
        self.motor_1.speed_def = 0.000005
        self.motor_1.enable_on(False)
        self.pump_1 = Pump('pumps_1', self.motor_1)
        self.pump_1_enable = True

        self.motor_2 = Motor('pumps_2',  pins.motor_p2_step, pins.motor_p2_dir, pins.motor_p1p2_enable)
        self.motor_2.speed_def = 0.000005
        self.motor_2.enable_on(False)
        self.pump_2 = Pump('pumps_2', self.motor_2)
        self.pump_2_enable = True
        self.pump_2.dir = -1
        
        self.mode_game = False
        self.level = 1
        self.turn_min = 0
        self.turn_max = 1000

        self.filler_run = False

        # self.statistic_pump_1 = int(neuron.memory_read('memory.txt','pump_1'))
        # self.statistic_pump_2 = int(neuron.memory_read('memory.txt', 'pump_2'))
        
        self.stop = False
        self.ready = False

        self.pump_1.motor.time_distance_2 = 0 
        self.pump_2.motor.time_distance_2 = 0

        app.window_cip.power_pumps.connect(self.run)


    def run(self):
        self.enable_motors(True)

        asyncio.run(self._all_pour_async(self.pump_1.ml, self.pump_2.ml))
        # asyncio.run(self._all_pour_async(-0.3, -0.3, stop = False))
        # QThread.sleep(1)
        # asyncio.run(self._all_pour_async2())

        self.enable_motors(False)


    def filler(self):
        self.filler_run = True

        self.enable_motors(True)

        ml_1 = app.window_filler.pump_value_1 
        ml_2 = app.window_filler.pump_value_2

        asyncio.run(self._all_pour_async(ml_1, ml_2))

        self.enable_motors(False)

        self.stop_pump.emit()


    def prepare(self):
        self.filler_run = False
        self.enable_motors(True)
        
        asyncio.run(self._all_pour_async(30, 30))

        self.enable_motors(False)


    def cip(self):
        self.filler_run = False

        self.enable_motors(True)

        asyncio.run(self._all_pour_async(1000, 1000))

        self.enable_motors(False)

    
    def enable_motors(self, value = False):
        self.motor_1.enable_on(value)
        self.motor_2.enable_on(value)

    
    def stop_pumps(self):
        self.stop2 = True

        self.pump_1.motor.stop = True
        self.pump_2.motor.stop = True

        self.enable_motors(False)

        self.motor_1.stop_for = True
        self.motor_2.stop_for = True


    async def _stop_pumps(self):
        self.pump_1.motor.time_distance_2 = 1
        self.pump_2.motor.time_distance_2 = 1

        while not self.stop2:
            if pins.button_stop.get_value():
                self.stop_pumps()

            if self.stop2 == True or (self.pump_1.ready == True and self.pump_2.ready == True):
                self.pump_1.motor.stop = True
                self.pump_2.motor.stop = True

                self.minus_pump.emit()

                raise asyncio.CancelledError()
            
            if self.filler_run:
                if self.pump_1.motor.time_distance >= self.pump_1.motor.time_distance_2:
                    self.pump_1.motor.time_distance_2 = self.pump_1.motor.time_distance + 1
                    self.bottle_1.emit()
                    #print(self.pump_1.motor.time_distance)

                if self.pump_2.motor.time_distance >= self.pump_2.motor.time_distance_2:
                    self.pump_2.motor.time_distance_2 = self.pump_2.motor.time_distance + 1 
                    #print(self.pump_2.motor.time_distance)
                    self.bottle_2.emit()

            await asyncio.sleep(0.1)

    
    async def _pour_async2(self, motor, turn):
        await motor._freq_async2(1000, 1, turn)


    async def _all_pour_async(self, turn1, turn2, stop = True):
        self.start_pump.emit()

        print( ' self.pump_1.motor.stop', self.pump_1.motor.stop,  self.pump_2.motor.stop)
        print( ' turn1, turn2', turn1,  turn2)

        self.stop2 = False
        self.pump_1.ready = False
        self.pump_2.ready = False

        tasks = []

        if stop == True:
            tasks.append(asyncio.create_task(self._stop_pumps()))

        # tasks.append(asyncio.create_task(self.pump_1.motor.test()))

        if turn1 != 0 and self.pump_1_enable:
            tasks.append(asyncio.create_task(self.pump_1._pour_async(turn1)))
        else:
            self.pump_1.ready = True
         
        if turn2 != 0 and self.pump_2_enable:
            tasks.append(asyncio.create_task(self.pump_2._pour_async(-turn2)))
        else:
            self.pump_2.ready = True

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()
        
    
    async def _all_pour_async2(self):
        print('START DOWN')

        self.stop2 = False
        self.pump_1.ready = False
        self.pump_2.ready = False

        tasks = []

        tasks.append(asyncio.create_task(self.pump_1._pour_async_down(True)))
        tasks.append(asyncio.create_task(self.pump_2._pour_async_down(True)))

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()
        
    