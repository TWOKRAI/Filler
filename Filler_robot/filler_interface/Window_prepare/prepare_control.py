from PyQt5.QtWidgets import QMainWindow
from Window_prepare.prepare import Ui_MainWindow 
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

from Window_filler.filler_conrtol import filler_window

from app import app


class Prepare_control(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        icon_size = QSize(50, 50)

        self.button_menu.setIcon(QIcon(f'Style_windows/icons_black/icons8-menu-100.png'))
        self.button_menu.setIconSize(icon_size)
        self.button_menu.clicked.connect(self.menu_window)

        self.menu_text = ['Начать', 'Start', 'Beginnen', '開始']
        self.button_calibr.clicked.connect(self.calibr)

        self.sort_button = False

        self.myprogressBar.setMinimum(0)
        self.myprogressBar.setMaximum(100) 

        self.value = 1
        self.myprogressBar.setValue(self.value)

        self.update()


    def menu_window(self):
        app.window_main_filler.show()
        self.hide()
    

    def calibr(self):
        self.value += 33
        self.myprogressBar.setValue(self.value)
        self.scenario(self.value)

        if self.value >= 100:
            app.window_filler.show()
            self.hide()


    def scenario(self, value):
        match value:
            case 34:
                self.label.setText(f"Hello")
            case 67:
                self.label.setText(f"Hello2")



window_prepare = Prepare_control()
