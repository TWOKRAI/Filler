from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject

from Raspberry.pins_table import pins

from Filler_robot.Monitor.motor_monitor import Motor_monitor


class Input_request(QThread):
    pin_values_updated = pyqtSignal(dict)
    show_error = pyqtSignal()
    close_error = pyqtSignal()
    error = pyqtSignal()
    no_error = pyqtSignal()

    starting = pyqtSignal()


    def __init__(self) -> None:
        super().__init__()
        self.running = True

        self.run_request = True
        self.time_request = 0.05

        self.button_error = False

        self.motor_monitor = Motor_monitor()

        self.button = False


    def run(self):
        self.running = True
    
        self.request()


    def stop(self):
        self.running = False


    def request(self):
        while self.running:
            try:
                if pins.button_stop.get_value():
                    self.button_error = True
                    self.show_error.emit()
                    self.error.emit()
                else:
                    if self.button_error == True:
                        self.close_error.emit()
                        self.no_error.emit()

                    self.button_error = False
                
                if pins.button.get_value():
                    self.motor_monitor.start()
                    self.starting.emit()
                    QThread.msleep(100)

        
            except Exception as e:
                print(f"Error reading pin values: {e}")

            QThread.msleep(int(self.time_request * 1000))
        

# input_request = Input_request()