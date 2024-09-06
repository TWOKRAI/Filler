from PyQt5.QtCore import QThread, pyqtSignal

from Server.database import DatabaseManager


class Data_request(QThread):
    update = pyqtSignal(tuple)
    button_start = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.running = False

        self.run_request = True
        self.time_request = 1000

        self.data_prev = None

        self.database = DatabaseManager('Server/myproject/db.sqlite3')


    def run(self):
        self.running = True
    
        self.request()


    def stop(self):
        self.running = False


    def request(self):
        self.database.create_connection()

        while self.running:
            data = self.database.read_data()

            if self.data_prev != None:
                for index, d in enumerate(data):
                    if d != self.data_prev[index]:
                        print(f'Изменилось c {self.data_prev[index]} на {d}')
                        self.update.emit(data)
                        self.data_prev = data
                        break
                    
                    
            
            if data[0] == 1:
                self.button_start.emit()
                data[0] = 0
                self.database.insert_data('status', 0)



           # self.data_prev = data

            QThread.msleep(int(self.time_request))
