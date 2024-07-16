from PyQt5.QtWidgets import QMainWindow
from Window_filler.filler import Ui_MainWindow  

from app import app


class filler_control(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)


        self.progressBar.setFormat("%v\nml")
        self.progressBar_2.setFormat("%v\nml")

        #self.button_calibr.clicked.connect(self.calibr)
        # self.button_game.clicked.connect(self.game)

        #window_setting.window_main = self
    

    def calibr(self):
        # window_setting.param_num = 0

        # window_setting.update()

        # window_setting.show()
        self.hide()

        print('start')
    
    
filler_window = filler_control()