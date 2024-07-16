from PyQt5.QtWidgets import QMainWindow
from Window_low.main_low import Ui_low
from PyQt5.QtCore import Qt

from app import app 

class low_control(QMainWindow, Ui_low):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)    


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


window_low = low_control()
