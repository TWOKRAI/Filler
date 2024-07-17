import gpiod
from gpiod.line import Direction, Value, Bias
import asyncio
import time

from motor import Motor


class Motor_monitor:
    def __init__(self):
        self.pin_motor_step = 6
        self.pin_motor_dir = 5
        self.pin_motor_enable = 4

        self.pin_button = 24
        self.pin_switch_out = 12
        self.pin_switch_in = 25

        self.motor = Motor(self.pin_motor_step, self.pin_motor_dir, self.pin_motor_enable)
        self.motor.speed = 0.0001

        self.chip = gpiod.Chip("/dev/gpiochip4")
        self.req = self.chip.request_lines(consumer="rpi-acloud-gpio-basic",
            config = {
                self.pin_button: gpiod.LineSettings(direction = Direction.INPUT),
                self.pin_switch_out: gpiod.LineSettings(direction = Direction.INPUT),
                self.pin_switch_in: gpiod.LineSettings(direction = Direction.INPUT),
            })

        self.distance = 10000
        self.direction = False

        self.stopped = False


    def run(self):
        button = self.req.get_value(self.pin_button)

        if button == Value.ACTIVE and self.direction == False:
            distance = self.distance
            asyncio.run(self._move_async(distance, detect = True))
            self.direction = not self.direction

        elif button == Value.ACTIVE and self.direction == True:
            distance = -self.distance
            asyncio.run(self._move_async(distance, detect = True))
            self.direction = not self.direction

    
    def get_output_value(self, pin, name):
        if self.req.get_value(pin) == Value.ACTIVE:
            print(f'{name} ON')
        else:
            print(f'{name} OFF')


    async def _detect_sensor(self):
        i = 0
        freedom_switch = False

        while True:
            if self.stopped:
                break

            switch_out = self.req.get_value(self.pin_switch_out)
            switch_in = self.req.get_value(self.pin_switch_in)

            if switch_out == Value.INACTIVE and switch_in == Value.INACTIVE:
                i += 1
                print(i)
                if i >= 15000: freedom_switch = True

            if (switch_out == Value.ACTIVE or switch_in == Value.ACTIVE) and freedom_switch:
                print('SWITCH')
                raise asyncio.CancelledError()
            
            if switch_out == Value.ACTIVE and self.direction == False:
                raise asyncio.CancelledError()
            
            await asyncio.sleep(0.0001)


    async def _move_async(self, distance, detect = False):
        self.stopped = False
        tasks = []

        if detect:
            sensor_task = asyncio.create_task(self._detect_sensor())
            tasks.append(sensor_task)

        tasks.append(asyncio.create_task(self.motor.move(distance, async_mode=True)))
            
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()

        self.stopped = True


motor_monitor = Motor_monitor()


while True:
    motor_monitor.run()
    print('ss')