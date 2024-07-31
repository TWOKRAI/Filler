from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont
import os

from Filler_interface.app import app


class Prepare_control(QMainWindow):
    def __init__(self):
        super().__init__()

        file_path = os.path.join('Filler_interface', 'Window_prepare', 'UI_prepare.ui')
        uic.loadUi(file_path, self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        icon_size = QSize(60, 60)
        button_size_1 = QSize(130, 120)
        button_size_2 = QSize(200, 120)

        font_1 = QFont()
        font_1.setFamily(app.font_family)
        font_1.setPointSize(25)
        font_1.setBold(False)
        font_1.setWeight(50)

        font_2 = QFont()
        font_2.setFamily(app.font_family)
        font_2.setPointSize(18)
        font_2.setBold(False)
        font_2.setWeight(50)

        self.label.setFont(font_1)
        self.label.setWordWrap(True)

        self.button_reset.setIconSize(icon_size)
        self.button_reset.setFixedSize(button_size_1)

        self.set_icons()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000) 
        self.timer.timeout.connect(self.on_timer_timeout)

        self.button_menu.clicked.connect(self.button_menu_clicked)
        self.button_menu.pressed.connect(self.button_menu_pressed)
        self.button_menu.released.connect(self.button_menu_released)

        self.button_reset.clicked.connect(self.show_popup)

        self.button_calibr.clicked.connect(self.button_calibr_clicked)
        self.button_calibr.setFont(font_2)
        self.button_calibr.setFixedSize(button_size_2)

        self.sort_button = False

        self.myprogressBar.setMinimum(0)
        self.myprogressBar.setMaximum(100) 

        self.value = 0
        self.myprogressBar.setValue(self.value)
      
        self.param_num = 0
        self.lang = 0

        self.update()


    def show(self):
        if app.on_fullscreen: self.fullscreen()

        super().show()

        self.reset()
        self.update_text()


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def language(self, lang):
        self.lang = lang

        self.update_text()


    def set_icons(self):
        self.button_reset_update()
        self.button_menu_update()
        
    
    def update_text(self):
        self.button_calibr_update()
        self.label_update()


    def show_popup(self):
        app.window_pop_up.hide()
        app.window_pop_up.show(self.reset)

        pop_show_text = {
            0: 'Вы хотите начать калибровку заново?',
            1: 'UUEOFERGPRPV{RVB{RB{BR}}}',
        }

        app.window_pop_up.label_2.setText(pop_show_text[self.lang])

    
    def button_reset_update(self):
        file_path = os.path.join('Filler_interface', 'Style_windows', 'icons_black', 'icons8-replay-100.png')
        self.button_reset.setIcon(QIcon(file_path))


    def reset(self):
        self.param_num = 0
        
        self.value = 0
        self.myprogressBar.setValue(self.value)

        self.update_text()


    def button_menu_update(self):
        icon_size = QSize(60, 60)
        self.button_menu.setIconSize(icon_size)

        button_size = QSize(130, 120)
        self.button_menu.setFixedSize(button_size)

        file_path = os.path.join('Filler_interface', 'Style_windows', 'icons_black', 'icons8-menu-100.png')
        self.button_menu.setIcon(QIcon(file_path))


    def button_menu_clicked(self):
        app.window_settings1.show()
        self.hide()


    def button_menu_pressed(self):    
        self.timer.start()


    def button_menu_released(self):
        self.timer.stop()
 
        
    def on_timer_timeout(self):
        app.window_main_filler.show()
        self.hide()
    

    def button_calibr_update(self):
        match self.param_num:
            case 0:
                name_button = {
                    0: 'Начать 1',
                    1: 'Start1',
                }

            case 1:
                name_button = {
                    0: 'Начать 2',
                    1: 'Start2',
                }

            case _:
                name_button = {
                    0: 'Начать 0',
                    1: 'Start0',
                }
        
        self.button_calibr.setText(name_button[self.lang])

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.button_calibr.setFont(font)

        button_size = QSize(200, 120)
        self.button_calibr.setFixedSize(button_size)
        

    def button_calibr_enable(self):
        pass 


    def button_calibr_clicked(self):
        self.param_num += 1

        self.label_update()
        self.button_calibr_update()

        self.myprogressBar.setValue(self.value)


    def label_update(self):
        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)

        self.label.setFont(font)
        self.label.setWordWrap(True)

        match self.param_num:
            case 0:
                label_name = {
                    0: 'Выставте руку робота в нулевую позицию и нажмите продолжить',
                    1: 'Выставте ttttку робота в нулевую позицию и нажмите продолжить',
                }

                self.label.setText(label_name[self.lang])
                
            case 1:
                label_name = {
                    0: 'Началась калибровка робота (Подождите)',
                    1: 'Началась rrrr калибровка робота (Подождите)',
                }
                                
                self.label.setText(label_name[self.lang])

                self.value += 33
            case 2:
                label_name = {
                    0: 'Поставьте стакан для розлива и нажмите стоп когда пойдет вода',
                    1: 'Поставьте rrrr стакан для розлива и нажмите стоп когда пойдет вода',
                }
                                
                self.label.setText(label_name[self.lang])

                self.value += 33
            case 3:
                label_name = {
                    0: 'Система готова. Нажмите продолжить',
                    1: 'Система готова444. Нажмите продолжить',
                }
                                
                self.label.setText(label_name[self.lang])

                self.value += 34
            case 4:
                app.window_filler.show()
                self.hide()
                self.param_num = 0
            case _:
                pass


window_prepare = Prepare_control()
