import asyncio

from Gadgets.MotorModules.motor import Motor
from Filler_robot.NeuroModules.neuron import neuron


class Pump:
    def __init__(self, name, motor):
        self.print_on = True

        self.name = name

        self.motor = motor

        self.motor.speed_def = 0.000005
        self.direction = True
        
        self.turn = 0
        self.ml = 50
        self.amount = 1
        self.step_amount = 350

        self.bottle_ml = 100
        self.bottle_min = 50

        self.warnning = False
        self.ready = False
    

    def ml_to_steps(self, ml):
        steps = int(ml / self.amount * self.step_amount)

        if self.print_on:
            print(f'pump {self.name}, ml_to_steps // output: steps = {steps}')

        return steps
    

    def step_to_ml(self):
        return int(self.motor.value * self.amount / self.step_amount)


    async def _pour_async(self, ml):
        self.turn = self.ml_to_steps(ml)

        self.motor.limit_min = -1 * (self.turn + 1000)
        self.motor.limit_max = self.turn + 1000
        
        if self.bottle_ml - ml >= ml:
            self.motor.null_value()

            # Создаем асинхронную задачу для вызова функции move мотора
            task = asyncio.create_task(self.motor.move(self.turn, async_mode=True))
            # Ожидаем завершения задачи
            await task

        else:
            self.warnning = True
            print(f'Pour {self.name}: WARNING')

        if self.print_on:
            print(f'Pour {self.name} : {self.turn}')

        self.ready = True
        

    def pour(self, ml):
        self.motor.value = 0
        self.motor.error_limit = False
        
        asyncio.run(self._pour_async(ml))
    

class Pump_station:
    def __init__(self): 
        self.motor_1 = Motor('pumps_1', 27, 22, 24)
        self.pump_1 = Pump('pumps_1', self.motor_1)

        self.motor_2 = Motor('pumps_2', 18, 23, 20)
        self.pump_2 = Pump('pumps_2', self.motor_2)
        
        self.mode_game = False
        self.level = 1
        self.turn_min = 0
        self.turn_max = 1000

        self.statistic_pump_1 = int(neuron.memory_read('memory.txt','pump_1'))
        self.statistic_pump_2 = int(neuron.memory_read('memory.txt', 'pump_2'))
        

    def run(self):
        asyncio.run(self._all_pour_async())
        self.statistic_write()


    def statistic_write(self):
        self.statistic_pump_1 += self.pump_1.step_to_ml()
        self.statistic_pump_2 += self.pump_2.step_to_ml()

        neuron.memory_write('memory.txt', 'pump_1', self.statistic_pump_1)
        neuron.memory_write('memory.txt', 'pump_2', self.statistic_pump_2)


    async def _all_pour_async(self):
        if self.mode_game == False:
            turn1 = self.pump_1.ml
            turn2 = self.pump_2.ml
        else:
            turn1 = game_ruletka.pour()
            turn2 = game_ruletka.pour()

        tasks = []

        if turn1 != 0:
            tasks.append(asyncio.create_task(self.pump_1._pour_async(turn1)))

        if turn2 != 0:
            tasks.append(asyncio.create_task(self.pump_2._pour_async(turn2)))

        await asyncio.gather(*tasks)


pump_station = Pump_station()
#pump_station.run()