
from PyQt5.QtCore import QTimer

from app import app


from Window_settings1.settings_control_copy import Control


class Control(Control):
    def __init__(self):
        super().__init__()

        self.font_text.setPointSize(21)
        self.label_window.setFont(self.font_text)
        self.label_window.setText('НАСТРОЙКИ СИСТЕМЫ')

        self.timer_exit = QTimer(self)
        self.timer_exit.setSingleShot(True)
        self.timer_exit.setInterval(6000) 
        self.timer_exit.timeout.connect(self.on_timer_reset)

        self.button_reset.pressed.connect(self.button_reset_pressed)
        self.button_reset.released.connect(self.button_reset_released)


    def button_reset_pressed(self):    
        self.timer_exit.start()


    def button_reset_released(self):
        self.timer_exit.stop()


    def on_timer_reset(self):
        app.exit()


    def get_parametrs(self): 
        self.param_list = {
            1: app.lang_num,
            2: app.styling.r_border,
            3: app.styling.g_border,
            4: app.styling.b_border,
            5: app.styling.r_icons_text,
            6: app.styling.g_icons_text,
            7: app.styling.b_icons_text,
        }


    def put_parametrs(self):
        app.lang_num = self.param_list[1]
        app.styling.r_border = self.param_list[2]
        app.styling.g_border = self.param_list[3]
        app.styling.b_border = self.param_list[4]
        app.styling.r_icons_text = self.param_list[5]
        app.styling.g_icons_text = self.param_list[6]
        app.styling.b_icons_text = self.param_list[7]

        print(app.lang_num)
       

    def default_parametrs(self):
        app.lang_num = '0'
        
        app.language()


    def set_parametrs(self): 
        self.window_name = {
            1: ['НАСТРОЙКИ СИСТЕМЫ', 'Statistic'],
            2: ['НАСТРОЙКИ СИСТЕМЫ', 'Statistic'],
            3: ['НАСТРОЙКИ СИСТЕМЫ', 'Statistic'],
            4: ['НАСТРОЙКИ СИСТЕМЫ', 'Statistic'],
            5: ['НАСТРОЙКИ СИСТЕМЫ', 'Statistic'],
            6: ['НАСТРОЙКИ СИСТЕМЫ', 'Statistic'],
            7: ['НАСТРОЙКИ СИСТЕМЫ', 'Statistic'],
        }   
                               
        self.param_name = {
            1: ['Язык', 'language', 'Sprache', '語言'],
            2: ['Цвет 1 (Контур)', 'language', 'Sprache', '語言'],
            3: ['Цвет 1 (Контур)', 'language', 'Sprache', '語言'],
            4: ['Цвет 1 (Контур)', 'language', 'Sprache', '語言'],
            5: ['Цвет 2 (Иконка)', 'language', 'Sprache', '語言'],
            6: ['Цвет 2 (Иконка)', 'language', 'Sprache', '語言'],
            7: ['Цвет 2 (Иконка)', 'language', 'Sprache', '語言'],
        }

        self.font_size = {
            1: {'window_name': 21, 'coll_params': 35, 'value': 60, 'value_mini': 30, 'name_params': 30,},
            2: {'window_name': 21, 'coll_params': 35, 'value': 60, 'value_mini': 30, 'name_params': 30,},
            3: {'window_name': 21, 'coll_params': 35, 'value': 60, 'value_mini': 30, 'name_params': 30,},
            4: {'window_name': 21, 'coll_params': 35, 'value': 60, 'value_mini': 30, 'name_params': 30,},
            5: {'window_name': 21, 'coll_params': 35, 'value': 60, 'value_mini': 30, 'name_params': 30,},
            6: {'window_name': 21, 'coll_params': 35, 'value': 60, 'value_mini': 30, 'name_params': 30,},
            7: {'window_name': 21, 'coll_params': 35, 'value': 60, 'value_mini': 30, 'name_params': 30,},
        }

        self.value_name_mini = {
            1: ['', '', '', '', ''],
            2: ['', '', '', '', ''],
            3: ['', '', '', '', ''],
            4: ['', '', '', '', ''],
            5: ['', '', '', '', ''],
            6: ['', '', '', '', ''],
            7: ['', '', '', '', ''],
        }

        self.value_min = {
            1: None,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
        }

        self.value_max = {
            1: None,
            2: 255,
            3: 255,
            4: 255,
            5: 255,
            6: 255,
            7: 255,
        }

        self.value_id = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
        }

        self.value_step = {
            1: ['0', '1', '2', '3'],
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1,
            7: 1,
        }

        self.value_name = {
            1: [['Русский', 'English', 'Deutsch', '中国人'], ['Русский', 'English', 'Deutsch', '中国人']],
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
        }

        self.color_text = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
        }
    

    def minus(self):
        super().minus()

        self.value_text()

        if self.param_num == 1:
            app.language()
        elif self.param_num == 2:
            app.recolor()
        elif self.param_num == 3:
            app.recolor()
        elif self.param_num == 4:
            app.recolor()
        elif self.param_num == 5:
            app.recolor()
        elif self.param_num == 6:
            app.recolor()
        elif self.param_num == 7:
            app.recolor()


    def minus_released(self):
        super().minus_released()

        if self.param_num == 2:
            app.icons_recolor()
            app.recolor()
        elif self.param_num == 3:
            app.icons_recolor()
            app.recolor()
        elif self.param_num == 4:
            app.icons_recolor()
            app.recolor()
        elif self.param_num == 5:
            app.icons_recolor()
            app.recolor()
        elif self.param_num == 6:
            app.icons_recolor()
            app.recolor()
        elif self.param_num == 7:
            app.icons_recolor()
            app.recolor()


    def plus(self):
        super().plus()

        self.value_text()

        if self.param_num == 1:
            app.language()
        elif self.param_num == 2:
            app.recolor()
        elif self.param_num == 3:
            app.recolor()
        elif self.param_num == 4:
            app.recolor()
        elif self.param_num == 5:
            app.recolor()
        elif self.param_num == 6:
            app.recolor()
        elif self.param_num == 7:
            app.recolor()
        

    def plus_released(self):
        super().plus_released()

        if self.param_num == 2:
            app.icons_recolor()
            app.recolor()
        elif self.param_num == 3:
            app.icons_recolor()
            app.recolor()
        elif self.param_num == 4:
            app.icons_recolor()
            app.recolor()
        elif self.param_num == 5:
            app.icons_recolor()
            app.recolor()
        elif self.param_num == 6:
            app.icons_recolor()
            app.recolor()
        elif self.param_num == 7:
            app.icons_recolor()
            app.recolor()

    
    def right(self):
        super().right()
        self.value_text()

    
    def left(self):
        super().left()
        self.value_text()


    def right_enable(self):
        if self.param_num >= len(self.param_list):
            self.button_right.setEnabled(False)
        else:
            self.button_right.setEnabled(True)

    
    def value_text(self):
        if self.param_num == 2:
            self.value.setText(f"R:{self.param_list[self.param_num]}")
        elif self.param_num == 3:
            self.value.setText(f"G:{self.param_list[self.param_num]}")
        elif self.param_num == 4:
            self.value.setText(f"B:{self.param_list[self.param_num]}")
        elif self.param_num == 5:
            self.value.setText(f"R:{self.param_list[self.param_num]}")
        elif self.param_num == 6:
            self.value.setText(f"G:{self.param_list[self.param_num]}")
        elif self.param_num == 7:
            self.value.setText(f"B:{self.param_list[self.param_num]}")


window_setting2 = Control()