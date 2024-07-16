from PyQt5.QtWidgets import QMainWindow
from Window_settings2.settings2 import Ui_MainWindow 
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from app import app


class Settings_control(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        icon_size = QSize(50, 50)

        self.button_menu.setIcon(QIcon(f'Style_windows/icons_black/icons8-menu-100.png'))
        self.button_menu.setIconSize(icon_size)

        self.button_menu.clicked.connect(self.menu)

        self.button_sort.setIcon(QIcon('Style_windows/icons_black/icons8-settings-100.png'))
        self.button_sort.setIconSize(icon_size)
        self.button_sort.clicked.connect(self.sort)

        
        self.button_left.setIcon(QIcon('Style_windows/icons_black/icons8-back-100.png'))
        self.button_left.setIconSize(icon_size)

        self.button_left.clicked.connect(self.left)

        
        self.button_right.setIcon(QIcon('Style_windows/icons_black/icons8-forward-100.png'))
        self.button_right.setIconSize(icon_size)

        self.button_right.clicked.connect(self.right)


        self.button_minus.setIcon(QIcon('Style_windows/icons_black/icons8-back-100.png'))
        self.button_minus.setIconSize(icon_size)

        self.button_minus.clicked.connect(self.minus)


        self.button_plus.setIcon(QIcon('Style_windows/icons_black/icons8-forward-100.png'))
        self.button_plus.setIconSize(icon_size)

        self.button_plus.clicked.connect(self.plus)

        self.lang = 0
        self.step = 5

        self.param_num = 0

        self.lang = 0
        self.lang_list = ['Русский', 'English', 'Deutsch', '中国人']
        self.param_list = ['Язык', 'language', 'Sprache', '語言']

        self.update()


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def menu(self):
        app.window_main_filler.show()
        self.hide()
    

    def sort(self):
        app.window_prepare.show()
        self.hide()


    def update(self):
        self.value.setText(f"{self.lang_list[self.lang]}")
        self.name_params.setText(f"{self.param_list[self.lang]}")

        text = f'{self.param_num + 1} / {len(self.param_list)}'
        self.coll_params.setText(text)


    def left(self):
        pass
        
    
    def right(self):
        pass


    def minus(self):
        self.lang -= 1

        if self.lang < 0:
            self.lang = 0

        app.language(self.lang_list[self.lang])

        self.update()


    def plus(self):
        self.lang += 1
        
        if self.lang > len(self.lang_list) - 1:
            self.lang = len(self.lang_list) - 1

        app.language(self.lang_list[self.lang])
        self.update()


window_setting2 = Settings_control()