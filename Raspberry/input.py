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



from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject

from Raspberry.pins_table import pins

from Filler_robot.Monitor.motor_monitor import Motor_monitor


class Input_request(QObject):
    pin_values_updated = pyqtSignal(dict)
    show_error = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.running = True

        self.run_request = True
        self.time_request = 0.1

        self.button_error = False

        self.motor_monitor = Motor_monitor()


    def run(self):
        self.request()


    def stop(self):
        self.running = False


    def request(self):
        self.running = True

        while self.running:
            try:
                if pins.switch_x.get_value():
                    self.button_error = True
                    self.show_error.emit()
                else:
                    self.button_error = False
                
                if pins.button.get_value():
                    self.motor_monitor.run()

            except Exception as e:
                print(f"Error reading pin values: {e}")

            QThread.msleep(int(self.time_request * 1000))


# input_request = Input_request()