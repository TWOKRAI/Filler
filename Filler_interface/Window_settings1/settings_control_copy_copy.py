from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont

from Filler_interface.app import app
from Lib.memory import Memory
from Filler_interface.filler import filler



class Control(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'Filler_interface\Window_settings1\UI_settings.ui', self)
       
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        icon_size = QSize(60, 60)
        button_size = QSize(130, 120)

        self.font_text = QFont()
        self.font_text.setFamily("Siemens AD Sans")
        self.font_text.setBold(False)
        self.font_text.setWeight(50)

        self.button_menu.setMinimumSize(button_size)
        self.button_menu.setIconSize(icon_size)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000) 
        self.timer.timeout.connect(self.on_timer_timeout)

        self.button_menu.clicked.connect(self.button_menu_clicked)
        self.button_menu.pressed.connect(self.button_menu_pressed)
        self.button_menu.released.connect(self.button_menu_released)

        self.button_reset.setMinimumSize(button_size)
        self.button_reset.setIconSize(icon_size)

        self.button_reset.clicked.connect(self.show_popup)

        self.timer_left_pressed = QTimer(self)
        self.timer_left_pressed.setInterval(int(300))
        self.timer_left_pressed.timeout.connect(self.left)

        self.button_left.setMinimumSize(button_size)
        self.button_left.setIconSize(icon_size)

        self.button_left.clicked.connect(self.left)
        self.button_left.pressed.connect(self.left_pressed)
        self.button_left.released.connect(self.left_released)

        self.timer_right_pressed = QTimer(self)
        self.timer_right_pressed.setInterval(int(300))
        self.timer_right_pressed.timeout.connect(self.right)
        
        self.button_right.setMinimumSize(button_size)
        self.button_right.setIconSize(icon_size)

        self.button_right.clicked.connect(self.right)
        self.button_right.pressed.connect(self.right_pressed)
        self.button_right.released.connect(self.right_released)

        self.step_button = 1

        self.timer_minus_pressed = QTimer(self)
        self.timer_minus_pressed.setInterval(int(200/self.step_button))
        self.timer_minus_pressed.timeout.connect(self.minus)

        self.button_minus.setMinimumSize(button_size)
        self.button_minus.setIconSize(icon_size)

        self.button_minus.clicked.connect(self.minus)
        self.button_minus.pressed.connect(self.minus_pressed)
        self.button_minus.released.connect(self.minus_released)

        self.timer_plus_pressed = QTimer(self)
        self.timer_plus_pressed.setInterval(int(200/self.step_button))
        self.timer_plus_pressed.timeout.connect(self.plus)

        self.button_plus.setMinimumSize(button_size)
        self.button_plus.setIconSize(icon_size)

        self.button_plus.clicked.connect(self.plus)
        self.button_plus.pressed.connect(self.plus_pressed)
        self.button_plus.released.connect(self.plus_released)

        self.set_icons()

        self.lang = 0
        self.step = 1

        self.param_num = 1
        self.value_id = 1

        self.param_list = []



    
    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        self.param_num = 1
        self.update()
        self.enable_control()
        super().show()


    def button_menu_clicked(self):
        app.window_main_filler.show()
        self.hide()
    

    def button_menu_pressed(self):    
        self.timer.start()


    def button_menu_released(self):
        self.timer.stop()


    def on_timer_timeout(self):
        print('Button was held down for 2 seconds!')
        app.window_main_filler.show()
        self.hide()


    def show_popup(self):
        app.window_pop_up.hide()
        app.window_pop_up.show(self.reset)


    def reset(self):
        self.default_parametrs()
        self.get_parametrs()
        self.memory.memory_read('data', self.param_list)

        self.update()
        self.enable_control()


    def language(self, lang):
        self.lang = int(lang)

        self.update()

    
    def set_icons(self):
        self.button_menu.setIcon(QIcon(r'Filler_interface\Style_windows/icons_black/icons8-menu-100.png'))
        self.button_reset.setIcon(QIcon(r'Filler_interface\Style_windows/icons_black/icons8-replay-100.png'))
        self.button_left.setIcon(QIcon(r'Filler_interface\Style_windows/icons_black/icons8-back-100.png'))
        self.button_right.setIcon(QIcon(r'Filler_interface\Style_windows/icons_black/icons8-forward-100.png'))
        self.button_minus.setIcon(QIcon(r'Filler_interface\Style_windows\icons_black\icons8-subtract-100.png'))
        self.button_plus.setIcon(QIcon(r'Filler_interface\Style_windows\icons_black\icons8-plus-math-100.png'))


    def put_parametrs(self):
       filler.param1 = self.param_list[1]
       filler.param2 = self.param_list[2]
       filler.param3 = self.param_list[3]
       filler.param4 = self.param_list[4]
       filler.param5 = self.param_list[5]
       filler.param6 = self.param_list[6]

       print(filler.param1, filler.param2, filler.param3, filler.param4)

    
    def get_parametrs(self): 
        self.param_list = {
            1: filler.param1,
            2: filler.param2,
            3: filler.param3,
            4: filler.param4,
            5: filler.param5,
            6: filler.param6,
            7: 'Готово',
        }


    def default_parametrs(self):
        pass
    

    def text_color(self):
        color = self.color_text[self.param_num]

        print('text_color')

        if color is not None:
            value_id = self.value_id[self.param_num]
            color = color[value_id]

            print(value_id, color)

            if color is not None:
                color = color
            else:
                color = app.styling.text_color
        else:
            color = app.styling.text_color


        style = f"color: rgb({color[0]}, {color[1]}, {color[2]});"
        
        self.value.setStyleSheet(style)


    def update(self):
        self.label_window_update()
        self.coll_params_update()
        self.value_update()
        self.value_mini_update()
        self.name_params_update()
    

    def enable_control(self):
        self.minus_enable()
        self.plus_enable()
        self.left_enable()
        self.right_enable()


    def label_window_update(self):
        pass


    def coll_params_update(self):
        pass


    def value_update(self):
        pass


    def value_mini_update(self):
        pass


    def name_params_update(self):
        pass


    def left(self):
        pass

    def left_pressed(self):
        self.timer_left_pressed.start()


    def left_released(self):
        self.timer_left_pressed.stop()

    
    def left_enable(self):
        pass
    

    def right(self):
        pass
    

    def right_pressed(self):
        self.timer_right_pressed.start()


    def right_released(self):
        self.timer_right_pressed.stop()

    
    def right_enable(self):
        pass


    def minus(self):
        self.timer_minus_pressed.setInterval(int(200/self.step_button))
        self.step_button += 0.1

        


    def minus_pressed(self):
        self.timer_minus_pressed.start()


    def minus_released(self):
        self.timer_minus_pressed.stop()
        self.step_button = 1


    def minus_enable(self):
        pass


    def plus(self):
        self.timer_plus_pressed.setInterval(int(200/self.step_button))
        self.step_button += 0.1

        self.enable_control()
    

    def plus_pressed(self):
        self.timer_plus_pressed.start()


    def plus_released(self):
        self.timer_plus_pressed.stop()
        self.step_button = 1


    def plus_enable(self):
        pass


window_setting = Control()