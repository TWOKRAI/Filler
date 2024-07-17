import gpiod
from gpiod.line import Direction, Value, Bias
import time


class Motor_monitor:
    def __init__(self):
        self.pin_motor_up = 6
        self.pin_motor_down = 5
        self.pin_button = 24
        self.pin_switch_up = 12
        self.pin_switch_down = 25

        self.chip = gpiod.Chip("/dev/gpiochip4")
        self.req = self.chip.request_lines(consumer="rpi-acloud-gpio-basic",
            config = {
                self.pin_button: gpiod.LineSettings(direction = Direction.INPUT),
                self.pin_switch_up: gpiod.LineSettings(direction = Direction.INPUT),
                self.pin_switch_down: gpiod.LineSettings(direction = Direction.INPUT),
                self.pin_motor_up: gpiod.LineSettings(direction = Direction.OUTPUT),
                self.pin_motor_down: gpiod.LineSettings(direction = Direction.OUTPUT),
            })

        self.req.set_value(self.pin_motor_up, Value.INACTIVE)
        self.req.set_value(self.pin_motor_down, Value.INACTIVE)

        self.direction = False
        self.button_front = False

    
    def start(self):
        if self.req.get_value(self.pin_switch_up) == Value.INACTIVE:
            
            

    
    def run(self):
        self.button_on = self.button()

        if self.button_on:
            self.motor_on(self.pin_motor_up)
            self.motor_on(self.pin_motor_up)

        self.no_switch = self.switch_no()

        if self.no_switch:
            self.motor_off(self.pin_motor_up, self.pin_switch_up)
            self.motor_off(self.pin_motor_down, self.pin_switch_down)

        # motor.motor_run(motor.pin_motor_up, 'pin_motor_up', motor.pin_switch_up, False)
        # motor.motor_run(motor.pin_motor_down,'pin_motor_down', motor.pin_switch_down, True)


    def button(self):
        if motor.req.get_value(motor.pin_button) == Value.ACTIVE and self.button_on == False:
            self.button_on = True
        
        if motor.req.get_value(motor.pin_button) == Value.INACTIVE:
            self.button_on = False
        
        return self.button_on


    def get_input_value(self, pin):
        if motor.req.get_value(pin) == Value.ACTIVE:
            print(f'{pin} ON')
        else:
            print(f'{pin} OFF')
    

    def motor_run(self, pin_output, name_output, pin_input, direction):
        if self.button_on and self.direction == direction:
            motor.req.set_value(pin_output, Value.ACTIVE)
            self.get_input_value(pin_output, name_output)
            time.sleep(1)

        if self.req.get_value(pin_input) == Value.ACTIVE:
            motor.req.set_value(pin_output, Value.INACTIVE)
            print(f'stop {name_output}')

            self.button_on = False
            time.sleep(1)

            self.direction = not self.direction


    def motor_on(self):
        if self.direction == False:
            self.req.set_value(self.pin_motor_up, Value.ACTIVE)
            self.get_input_value(self.pin_motor_up)
        else:
            self.req.set_value(self.pin_motor_down, Value.ACTIVE)
            self.get_input_value(self.pin_motor_down)


    def motor_off(self, pin_motor, pin_switch):
        motor_run = self.req.get_value(pin_motor)
        switch_on = self.req.get_value(pin_switch)

        if motor_run == Value.ACTIVE and switch_on == Value.ACTIVE:
            self.req.set_value(pin_motor, Value.INACTIVE) 
            self.direction = not self.direction
    

    def switch_no(self):
        switch_1 = self.req.get_value(self.pin_switch_up)
        switch_2 = self.req.get_value(self.pin_switch_down)

        if switch_1 == Value.INACTIVE and switch_2 == Value.INACTIVE:
            return True
        else:
            return False




    # def motor_run_up(self):
    #     if motor.req.get_value(motor.pin_button) == Value.ACTIVE and self.run == False:
    #         motor.req.set_value(motor.pin_motor_up, Value.ACTIVE)
    #         self.get_value(motor.pin_motor_up, 'pin_motor_up')
    #         time.sleep(1)

    #     if self.req.get_value(self.pin_switch_up) == Value.ACTIVE:
    #         motor.req.set_value(motor.pin_motor_up, Value.INACTIVE)
    #         self.run = True
    #         print('stop UP')
    #         time.sleep(1)

    
    # def motor_run_down(self):
    #     if motor.req.get_value(motor.pin_button) == Value.ACTIVE and self.run == True:
    #         motor.req.set_value(motor.pin_motor_down, Value.ACTIVE)
    #         self.get_value(motor.pin_motor_down, 'pin_motor_down')
    #         time.sleep(1)

    #     if self.req.get_value(self.pin_switch_down) == Value.ACTIVE:
    #         motor.req.set_value(motor.pin_motor_down, Value.INACTIVE)
    #         self.run = False
    #         print('stop DOWN')
    #         time.sleep(1)


motor = Motor_monitor()


while True:
    motor.run()

    #motor.req.set_value(motor.pin_motor_up, Value.INACTIVE)

    # for i in range(1000):
    #     motor.req.set_value(motor.pin_motor_up, Value.ACTIVE)
    #     time.sleep(0.001)
    #     motor.req.set_value(motor.pin_motor_up, Value.INACTIVE)
    #     time.sleep(0.001)



    # motor.req.set_value(motor.pin_motor_up, Value.ACTIVE)
    # time.sleep(2)
    # motor.req.set_value(motor.pin_motor_up, Value.INACTIVE)
 

    # motor.req.set_value(motor.pin_motor_down, Value.ACTIVE)
    # time.sleep(2)
    # motor.req.set_value(motor.pin_motor_down, Value.INACTIVE)


    # time.sleep(2)
    # motor.req.set_value(motor.pin_motor_down, Value.ACTIVE)

    # time.sleep(2)
    # motor.req.set_value(motor.pin_motor_down, Value.INACTIVE)
    # time.sleep(2)
    



    # if motor.req.get_value(motor.pin_switch_down) == Value.ACTIVE:
    #     print(f'pin_switch_down {motor.req.get_value(motor.pin_switch_down)}')
    
    # if motor.req.get_value(motor.pin_switch_up) == Value.ACTIVE:
    #     print(f'pin_switch_up {motor.req.get_value(motor.pin_switch_up)}')
    
    # if motor.req.get_value(motor.pin_button) == Value.ACTIVE:
    #     print(f'pin_button {motor.req.get_value(motor.pin_button)}')




    #time.sleep(1)