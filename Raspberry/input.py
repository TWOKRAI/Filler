from PyQt5.QtCore import QThread, pyqtSignal
from pins_table import pins


class Input_request(QThread):
    pin_values_updated = pyqtSignal(dict)

    def __init__(self) -> None:
        super().__init__()
        self.running = True

        self.run_request = True
        self.time_request = 0.05

    def run(self):
        self.request()

    def stop(self):
        self.running = False

    def request(self):
        while self.running:
            try:
                if self.run_request:
                    values = {
                        'button': pins.get_value(pins.button),
                        'button_stop': pins.get_value(pins.button_stop),
                        'switch_x': pins.get_value(pins.switch_x)
                    }

                    self.pin_values_updated.emit(values)
            except Exception as e:
                print(f"Error reading pin values: {e}")

            QThread.sleep(self.time_request)


input_request = Input_request()