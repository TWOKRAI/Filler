from PyQt5.QtWidgets import QMainWindow, QPushButton
from Filler_interface.Window_low.main_low import Ui_low
from PyQt5.QtCore import Qt

from Filler_interface.app import app 


class low_control(QMainWindow, Ui_low):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)  
      
        self.button = QPushButton(self)
        self.button.setObjectName("Button_close")
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.raise_()

        self.button.clicked.connect(self.close)

    
    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        super().show()

    
    def close(self):
        app.window_main_filler.hide()
        app.window_main_filler.show()


window_low = low_control()
