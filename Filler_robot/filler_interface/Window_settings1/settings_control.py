from PyQt5.QtWidgets import QMainWindow
from Window_settings1.settings import Ui_MainWindow 
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from app import app

from filler import filler


class Settings_control(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        icon_size = QSize(50, 50)

        self.button_menu.setIcon(QIcon(f'FILLER INTERFACE/Style_windows/icons_black/icons8-menu-100.png'))
        self.button_menu.setIconSize(icon_size)

        self.button_menu.clicked.connect(self.back_window)

        self.button_sort.setIcon(QIcon('FILLER INTERFACE/Style_windows/icons_black/icons8-settings-100.png'))
        self.button_sort.setIconSize(icon_size)
        self.button_sort.clicked.connect(self.sort)

        
        self.button_left.setIcon(QIcon('FILLER INTERFACE/Style_windows/icons_black/icons8-back-100.png'))
        self.button_left.setIconSize(QSize(60, 60))

        self.button_left.clicked.connect(self.left)

        
        self.button_right.setIcon(QIcon('FILLER INTERFACE/Style_windows/icons_black/icons8-forward-100.png'))
        self.button_right.setIconSize(icon_size)

        self.button_right.clicked.connect(self.right)


        self.button_minus.setIcon(QIcon('FILLER INTERFACE/Style_windows\icons_black\icons8-subtract-100.png'))
        self.button_minus.setIconSize(icon_size)

        self.button_minus.clicked.connect(self.minus)


        self.button_plus.setIcon(QIcon('FILLER INTERFACE/Style_windows\icons_black\icons8-plus-math-100.png'))
        self.button_plus.setIconSize(icon_size)

        self.button_plus.clicked.connect(self.plus)


        self.lang = 0
        self.step = 5

        self.param_num = 0

        self.param_list = [[filler.param1, 10, 100, 'Объем 1 /мл', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升', 'Көлемі 1 /ml'],
                [filler.param2, 30, 120, 'Объем 2 /мл', 'Volume 2 /ml', 'Volumen 2 /ml', '體積 2 /毫升', 'Көлемі 2 /ml']
            ]
        
        self.update()


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)

    
    def language(self, lang):
        self.lang = lang


    def set_params(self):
       filler.param1 = self.param_list[0][0]
       filler.param2 = self.param_list[1][0]

       print(filler.param1, filler.param2)


    def back_window(self):
        app.window_main_filler.show()
        self.hide()
    

    def sort(self):
        app.window_prepare.show()
        self.hide()


    def update(self):
        self.value.setText(f"{self.param_list[self.param_num][0]}")
        self.name_params.setText(f"{self.param_list[self.param_num][3 + self.lang]}")

        text = f'{self.param_num + 1} / {len(self.param_list)}'
        self.coll_params.setText(text)


    def left(self):
        self.param_num -= 1
        
        if self.param_num < 0:
            self.param_num = 0

        self.update()
        
    
    def right(self):
        self.param_num += 1
        
        if self.param_num > len(self.param_list) - 1:
            self.param_num = len(self.param_list) - 1

            app.window_prepare.show()
            self.hide()


        self.update()


    def minus(self):
        value = self.param_list[self.param_num][0]
        limit = self.param_list[self.param_num][1]
        
        if value > limit:
            value -= self.step

        self.value.setText(f"{value}")

        self.param_list[self.param_num][0] = value

        self.set_params()
        

    def plus(self):
        value = self.param_list[self.param_num][0]
        limit = self.param_list[self.param_num][2]

        if value < limit:
            value += self.step

        self.value.setText(f"{value}")

        self.param_list[self.param_num][0] = value

        self.set_params()


window_setting = Settings_control()