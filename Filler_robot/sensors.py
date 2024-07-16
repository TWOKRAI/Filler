    
import gpiod
from gpiod.line import Direction, Value, Bias



class Sensor():
    def __init__(self, name, pin_input, in_out) -> None:
        self.pin_input = pin_input

        self.chip = gpiod.Chip("/dev/gpiochip4")

        self.req = self.chip.request_lines(consumer="rpi-acloud-gpio-input",
            config={
                pin_input: gpiod.LineSettings(direction = Direction.INPUT)
            })


    def read_input(self):
            input_value = self.req.get_value(self.pin_input)

            if input_value == Value.ACTIVE:
                return True
            else:
                return False


sensor_limit_x = Sensor("detect-limit-x", 12, 'input')