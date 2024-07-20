import gpiod
from gpiod.line import Direction, Value

import tkinter as tk


class Pins():
    def __init__(self):
        self.motor_step = 26
        self.motor_dir = 19
        self.motor_enable = 13

        self.button_stop = 14
        self.button = 5
        self.switch_out = 8
        self.switch_in = 6

        self.switch_x = 25

        self.motor_x_step = 22
        self.motor_x_dir = 27
        self.motor_x_enable = 17

        self.motor_y_step = 4
        self.motor_y_dir = 3
        self.motor_y_enable = 2

        self.motor_z_step = 21
        self.motor_z_dir = 20
        self.motor_z_enable = 16

        self.motor_p1_step = 18
        self.motor_p1_dir = 15
         
        self.motor_p2_step = 23
        self.motor_p2_dir = 24

        self.motor_p1p2_enable = 7

        self.chip = gpiod.Chip("/dev/gpiochip4")
        self.req = self.chip.request_lines(consumer="rpi-acloud-gpio-basic",
            config = {
                self.button: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.button_stop: gpiod.LineSettings(direction = Direction.OUTPUT),
                
                self.switch_out: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.switch_in: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.switch_x: gpiod.LineSettings(direction = Direction.OUTPUT),

                self.motor_step: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.motor_dir: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.motor_enable: gpiod.LineSettings(direction = Direction.OUTPUT),

                self.motor_x_step: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.motor_x_dir: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.motor_x_enable: gpiod.LineSettings(direction = Direction.OUTPUT),

                self.motor_y_step: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.motor_y_dir: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.motor_y_enable: gpiod.LineSettings(direction = Direction.OUTPUT),

                self.motor_z_step: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.motor_z_dir: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.motor_z_enable: gpiod.LineSettings(direction = Direction.OUTPUT),

                self.motor_p1_step: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.motor_p1_dir: gpiod.LineSettings(direction = Direction.OUTPUT),

                self.motor_p2_step: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.motor_p2_dir: gpiod.LineSettings(direction = Direction.OUTPUT),

                self.motor_p1p2_enable: gpiod.LineSettings(direction = Direction.OUTPUT),
            })


    def get_value(self, pin, log = False):
        if self.req.get_value(pin) == Value.ACTIVE:
            if log: print(f'pin: {pin} - ON')
            return True
        elif self.req.get_value(pin) == Value.INACTIVE:
            if log: print(f'pin: {pin} - OFF')
            return False


    def set_value(self, pin, value):
        if value == True:
            self.req.set_value(pin, Value.ACTIVE)
        else:
            self.req.set_value(pin, Value.INACTIVE)


pins = Pins()

        
