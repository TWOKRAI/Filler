from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QFont

from Lib.memory import Memory
from Filler_interface.app import app

from Filler_interface.Window_settings1.settings_control_copy_copy import Control


class Control(Control):
    def __init__(self):
        super().__init__()
        
        self.timer_exit = QTimer(self)
        self.timer_exit.setSingleShot(True)
        self.timer_exit.setInterval(6000) 
        self.timer_exit.timeout.connect(self.on_timer_reset)

        self.button_reset.pressed.connect(self.button_reset_pressed)
        self.button_reset.released.connect(self.button_reset_released)

        self.param_list = {}
        self.memory = Memory(db_path=r'Filler_interface\Window_settings2\Data',  db_file='memory_db')
        

        self.get_parametrs()
        
        print('wwwwww',self.param_list)

        self.update()
        self.enable_control()


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
    

    def button_reset_pressed(self):    
        self.timer_exit.start()


    def button_reset_released(self):
        self.timer_exit.stop()


    def on_timer_reset(self):
        app.exit()

    
    def parametrs(self):
        self.param_list = {
            1: app.lang_num,
            2: app.styling.r_border,
            3: app.styling.g_border,
            4: app.styling.b_border,
            5: app.styling.r_icons_text,
            6: app.styling.g_icons_text,
            7: app.styling.b_icons_text,
            8: app.styling.r_text,
            9: app.styling.g_text,
            10: app.styling.b_text,
        }

        return self.param_list


    def get_parametrs(self): 
        self.param_list = self.parametrs()
        self.param_list = self.memory.memory_read('data', self.param_list)


    def put_parametrs(self):
        self.param_list = self.parametrs()
        self.memory.memory_write('data', self.param_list)


    def default_parametrs(self):
        app.lang_num = 0
        app.styling.r_border = 108
        app.styling.g_border = 161
        app.styling.b_border = 141
        app.styling.r_icons_text = 108
        app.styling.g_icons_text = 161
        app.styling.b_icons_text = 141
        app.styling.r_text = 108
        app.styling.g_text = 161
        app.styling.b_text = 141
        

        self.put_parametrs()
        self.get_parametrs()
        
        app.language()
        app.icons_recolor()
        app.recolor()
    

    def label_window_update(self):
        match self.param_num:
            case 1:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case 2:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case 3:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case 4:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case 5:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case 6:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case 7:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case _:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
        
        text = text[self.lang]
        self.label_window.setText(str(text))

        font = QFont()
        font.setFamily("Siemens AD Sans")
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.label_window.setFont(font)


    def coll_params_update(self):
        size_text = 21
        
        text = f'{self.param_num} / {10}'
        self.coll_params.setText(str(text))

        font = QFont()
        font.setFamily("Siemens AD Sans")
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.coll_params.setFont(font)


    def value_update(self):
        print('wwwwfwqfqgq', self.param_list)
        value = self.param_list[self.param_num]

        match self.param_num:
            case 1:
        
                value_text = {0: 'Русский', 
                              1: 'English', 
                              2: 'Deutsch', 
                              3: '中国人',
                              }

                value = value_text[int(value)]

                size_text = 60
            case 2:

                value = f"R:{value}"

                size_text = 60
            case 3:

                value = f"G:{value}"

                size_text = 60
            case 4:
 
                value = f"B:{value}"

                size_text = 60
            case 5:

                value = f"R:{value}"

                size_text = 60
            case 6:

                value = f"G:{value}"

                size_text = 60
            case 7:

                value = f"B:{value}"

                size_text = 60
            case 8:

                value = f"R:{value}"

                size_text = 60
            case 9:

                value = f"G:{value}"

                size_text = 60
            case 10:

                value = f"B:{value}"

                size_text = 60
            case _:
                value = None

                size_text = 60
        
        self.value.setText(str(value))

        font = QFont()
        font.setFamily("Siemens AD Sans")
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.value.setFont(font)
    
    
    def value_mini_update(self):
        match self.param_num:
            case 1:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 2:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 3:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 4:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 5:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 6:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 7:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case _:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
        
        text = text[self.lang]
        self.value_mini.setText(str(text))

        font = QFont()
        font.setFamily("Siemens AD Sans")
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.value_mini.setFont(font)


    def name_params_update(self):
        match self.param_num:
            case 1:
                text = {
                    0: 'Язык',
                    1: 'language',
                    2: 'Sprache',
                    3: '語言',
                }

                size_text = 30
            case 2:
                text = {
                    0: 'Цвет 1 (Контур)',
                    1: 'Цвет 12 (Контур)',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 3:
                text = {
                    0: 'Цвет 1 (Контур)',
                    1: 'Цвет 12 (Контур)',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 4:
                text = {
                    0: 'Цвет 1 (Контур)',
                    1: 'Цвет 12 (Контур)',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 5:
                text = {
                    0: 'Цвет 2 (Иконка)',
                    1: 'Цвет 21 (Иконка)',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 6:
                text = {
                    0: 'Цвет 2 (Иконка)',
                    1: 'Цвет 21 (Иконка)',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 7:
                text = {
                    0: 'Цвет 2 (Иконка)',
                    1: 'Цвет 21 (Иконка)',
                    2: '',
                    3: '',
                }

                size_text = 30

            case 8:
                text = {
                    0: 'Цвет 3 (Текст)',
                    1: 'Цвет 31 (Текст)',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 9:
                text = {
                    0: 'Цвет 2 (Текст)',
                    1: 'Цвет 21 (Текст)',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 10:
                text = {
                    0: 'Цвет 2 (Текст)',
                    1: 'Цвет 21 (Текст)',
                    2: '',
                    3: '',
                }

                size_text = 30
            case _:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
        
        text = text[self.lang]
        self.name_params.setText(str(text))

        font = QFont()
        font.setFamily("Siemens AD Sans")
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.name_params.setFont(font)


    def minus(self):
        super().minus()

        self.enable_control()

        match self.param_num:
            case 1:
                if app.lang_num > 0:
                    app.lang_num -= 1
                app.language()

            case 2:
                if app.styling.r_border > 0:
                    app.styling.r_border -= 1
                app.recolor()

            case 3:
                if app.styling.g_border > 0:
                    app.styling.g_border -= 1
                app.recolor()

            case 4:
                if app.styling.b_border > 0:
                    app.styling.b_border -= 1
                app.recolor()

            case 5:
                if app.styling.r_icons_text > 0:
                    app.styling.r_icons_text -= 1
                app.recolor()

            case 6:
                if app.styling.g_icons_text > 0:
                    app.styling.g_icons_text -= 1
                app.recolor()

            case 7:
                if app.styling.b_icons_text > 0:
                    app.styling.b_icons_text -= 1
                app.recolor()

            case 8:
                if app.styling.r_text > 0:
                    app.styling.r_text -= 1
                app.recolor()

            case 9:
                if app.styling.g_text > 0:
                    app.styling.g_text -= 1
                app.recolor()

            case 10:
                if app.styling.b_text > 0:
                    app.styling.b_text -= 1
                app.recolor()
        
        self.parametrs() 
        self.update()
        self.enable_control()
       
        
    def minus_released(self):
        super().minus_released()

        match self.param_num:
            case 1:
                pass

            case 2:
                app.icons_recolor()
                app.recolor()

            case 3:
                app.icons_recolor()
                app.recolor()

            case 4:
                app.icons_recolor()
                app.recolor()

            case 5:
                app.icons_recolor()
                app.recolor()

            case 6:
                app.icons_recolor()
                app.recolor()

            case 7:
                app.icons_recolor()
                app.recolor()

            case 8:
                app.icons_recolor()
                app.recolor()

            case 9:
                app.icons_recolor()
                app.recolor()

            case 10:
                app.icons_recolor()
                app.recolor()

        self.put_parametrs()


    def minus_enable(self):
        match self.param_num:
            case 1:
                print('ssssssssssssssssssssssssssssssss',app.lang_num)
                if app.lang_num <= 0:
                    self.button_minus.setEnabled(False)
                    print(12222)
                else:
                    self.button_minus.setEnabled(True)

            case 2:
                if app.styling.r_border <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 3:
                if app.styling.g_border <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 4:
                if app.styling.b_border <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 5:
                if app.styling.r_icons_text <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 6:
                if app.styling.g_icons_text <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 7:
                if app.styling.b_icons_text <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 8:
                if app.styling.r_text <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 9:
                if app.styling.g_text <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 10:
                if app.styling.b_text <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)


    def plus(self):
        super().plus()

        self.enable_control()

        match self.param_num:
            case 1:
                if app.lang_num < 4:
                    app.lang_num += 1
                app.language()

            case 2:
                if app.styling.r_border < 255:
                    app.styling.r_border += 1
                app.recolor()

            case 3:
                if app.styling.g_border < 255:
                    app.styling.g_border += 1
                app.recolor()

            case 4:
                if app.styling.b_border < 255:
                    app.styling.b_border += 1
                app.recolor()

            case 5:
                if app.styling.r_icons_text < 255:
                    app.styling.r_icons_text += 1
                app.recolor()

            case 6:
                if app.styling.g_icons_text < 255:
                    app.styling.g_icons_text += 1
                app.recolor()

            case 7:
                if app.styling.b_icons_text < 255:
                    app.styling.b_icons_text += 1
                app.recolor()

            case 8:
                if app.styling.r_text < 255:
                    app.styling.r_text += 1
                app.recolor()

            case 9:
                if app.styling.g_text < 255:
                    app.styling.g_text += 1
                app.recolor()

            case 10:
                if app.styling.b_text < 255:
                    app.styling.b_text += 1
                app.recolor()
        
        self.parametrs() 
        
        self.update()
        self.enable_control()
    

    def plus_released(self):
        super().plus_released()

        match self.param_num:
            case 1:
                pass

            case 2:
                app.icons_recolor()
                app.recolor()

            case 3:
                app.icons_recolor()
                app.recolor()

            case 4:
                app.icons_recolor()
                app.recolor()

            case 5:
                app.icons_recolor()
                app.recolor()

            case 6:
                app.icons_recolor()
                app.recolor()

            case 7:
                app.icons_recolor()
                app.recolor()

            case 8:
                app.icons_recolor()
                app.recolor()

            case 9:
                app.icons_recolor()
                app.recolor()

            case 10:
                app.icons_recolor()
                app.recolor()

        self.put_parametrs()


    def plus_enable(self):
        match self.param_num:
            case 1:
                if int(app.lang_num) >= 3:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 2:
                if app.styling.r_border >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 3:
                if app.styling.g_border >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 4:
                if app.styling.b_border >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 5:
                if app.styling.r_icons_text >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 6:
                if app.styling.g_icons_text >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 7:
                if app.styling.b_icons_text >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 8:
                if app.styling.r_text >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 9:
                if app.styling.g_text >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 10:
                if app.styling.b_text >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

    
    def left(self):
        if self.param_num > 1:
            self.param_num -= 1

        print(self.param_num)

        self.enable_control()
        self.update()
     

    def left_enable(self):
        if self.param_num <= 1:
            self.button_left.setEnabled(False)
        else:
            self.button_left.setEnabled(True)
    

    def right(self):
        if self.param_num < len(self.param_list):
            self.param_num += 1

        self.enable_control()
        self.update()


    def right_enable(self):
        if self.param_num >= 10:
            self.button_right.setEnabled(False)
        else:
            self.button_right.setEnabled(True)


window_setting2 = Control()