# from PyQt5.QtCore import QThread, pyqtSignal
# from pins_table import pins


# class Input_request(QThread):
#     pin_values_updated = pyqtSignal(dict)

#     def __init__(self) -> None:
#         super().__init__()
#         self.running = True

#         self.run_request = True
#         self.time_request = 0.05

#     def run(self):
#         self.request()

#     def stop(self):
#         self.running = False

#     def request(self):
#         while self.running:
#             try:
#                 if self.run_request:
#                     values = {
#                         'button': pins.get_value(pins.button),
#                         'button_stop': pins.get_value(pins.button_stop),
#                         'switch_x': pins.get_value(pins.switch_x)
#                     }

#                     self.pin_values_updated.emit(values)
#             except Exception as e:
#                 print(f"Error reading pin values: {e}")

#             QThread.msleep(int(self.time_request * 1000))


# input_request = Input_request()



from PyQt5.QtCore import QThread, pyqtSignal

class Input_request(QThread):
    pin_values_updated = pyqtSignal(dict)
    show_error = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.running = True

        self.run_request = True
        self.time_request = 0.05

        self.t1 = False

    def run(self):
        self.request()

    def stop(self):
        self.running = False

    def request(self):
        i = 0
        while self.running:
            try:
                if self.run_request:
                    i += 1
                    print(i)

                    if i == 100:
                        self.t1 = True
                        self.show_error.emit()
                    if i == 200:
                        self.t1 = False
                        i = 0

            except Exception as e:
                print(f"Error reading pin values: {e}")

            QThread.msleep(int(self.time_request * 1000))


input_request = Input_request()