from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QSize, QTimer, QThread
from PyQt5.QtGui import QFont, QIcon
import os

from Filler_interface.app import app

from Filler_interface.threads import thread

try:
    # from Filler_robot.NeuroModules.interface import interface
    from Filler_robot.robot_main import Robot_filler

    from Raspberry.input import Input_request

    raspberry = True
except ImportError:
    raspberry = False


class filler_control(QMainWindow):
    def __init__(self):
        super().__init__()

        file_path = os.path.join('Filler_interface', 'Window_filler', 'UI_filler.ui')
        uic.loadUi(file_path, self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.window_name = 'filler'

        icon_size = QSize(50, 50)
        button_size = QSize(190, 110)

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)


        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000) 
        self.timer.timeout.connect(self.on_timer_timeout)

        self.button_menu.setMinimumSize(button_size)
        self.button_menu.setIconSize(icon_size)
        self.button_menu.setFont(font)
        

        self.button_menu.clicked.connect(self.button_menu_clicked)
        self.button_menu.pressed.connect(self.button_menu_pressed)
        self.button_menu.released.connect(self.button_menu_released)
       

        self.button_pause.clicked.connect(self.button_pause_clicked)

        self.button_view.clicked.connect(self.button_view_clicked)

    
        self.lang = 0
        self.code = 0

        self.play = False


        self.thread_robot = QThread()
        self.robot_filler = None

        self.thread_input = QThread()
        self.input = None

        self.update()

        # self.start_input_thread()


    def start_robot_thread(self):
        if not self.thread_robot.isRunning():
            self.thread_robot = QThread()
            self.robot_filler = Robot_filler(robot_on = True)
            self.robot_filler.moveToThread(self.thread_robot)
            self.thread_robot.started.connect(self.robot_filler.run)
            self.robot_filler.interface.frame_captured.connect(app.window_view.update_frame)
            self.input_request.error.connect(self.robot_filler.robot.stop_motors)
            self.input_request.error.connect(app.window_view.close)
            self.thread_robot.start()
    

    def stop_robot_thread(self):
        if self.thread_robot is not None and self.thread_robot.isRunning():
            self.robot_filler.stop()
            self.thread_robot.quit()
            self.thread_robot.wait()
            # self.thread_robot = None
            # self.robot_filler = None


    def start_input_thread(self):
        if not self.thread_robot.isRunning():
            self.thread_input = QThread()
            self.input_request = Input_request()
            self.input_request.moveToThread(self.thread_input)
            self.thread_input.started.connect(self.input_request.run)

            self.input_request.show_error.connect(app.window_error.show)
            

            self.input_request.motor_monitor.on_signal.connect(app.window_start.close)
            self.input_request.motor_monitor.off_signal.connect(app.window_start.show)
            self.input_request.motor_monitor.off_signal.connect(app.window_view.close)
            self.input_request.motor_monitor.off_signal.connect(self.stop_input_thread)

            self.thread_input.start()
    

    def stop_input_thread(self):
        if self.thread_robot is not None and self.thread_robot.isRunning():
            self.input_request.stop()
            self.thread_input.quit()
            self.thread_input.wait()
            # self.thread_robot = None
            # self.robot_filler = None


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        super().show()

        self.update()

        app.window_focus = self.window_name
        print(app.window_focus)
        app.close_windows()

        self.play = True

        # if raspberry:
        #     self.robot_filler.enable_robot_on(True)

    
    def language(self, lang):
        self.lang = lang

        self.update()


    def update(self):
        self.button_menu_update()
        self.button_pause_update()
        self.button_view_update()
        self.progressBar_1_update()
        self.progressBar_2_update()
        self.value_1_update()
        self.value_2_update()
        self.label_update()
        self.label_drink_1_update()
        self.label_drink_2_update()
        self.label_value_1_update()
        self.label_value_2_update()


    def button_menu_update(self):        
        button_size = QSize(130, 120)
        self.button_menu.setFixedSize(button_size)

        icon_size = QSize(60, 60)
        self.button_menu.setIconSize(icon_size)
        
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


    
    def button_pause_update(self):
        button_size = QSize(130, 120)
        self.button_pause.setFixedSize(button_size)
    
        icon_size = QSize(70, 70)
        self.button_pause.setIconSize(icon_size)

        print(self.play)

        if self.play == True:
            file_path = os.path.join('Filler_interface', 'Style_windows', 'icons_black', 'icons8-pause-button-100.png')
            self.button_pause.setIcon(QIcon(file_path))

            # if raspberry:
            #     self.robot_filler.enable_robot_on(True)
        else:
            file_path = os.path.join('Filler_interface', 'Style_windows', 'icons_black', 'icons8-circled-play-100.png')
            self.button_pause.setIcon(QIcon(file_path))

            # if raspberry:
            #     self.robot_filler.enable_robot_on(False)


    def button_pause_clicked(self):
        self.play = not self.play
        print('PAUSE')

        self.button_pause_update()
        self.progressBar_recolor()
    

    def button_view_update(self):
        button_size = QSize(130, 120)
        self.button_view.setFixedSize(button_size)
    
        icon_size = QSize(60, 60)
        self.button_view.setIconSize(icon_size)

        file_path = os.path.join('Filler_interface', 'Style_windows', 'icons_black', 'icons8-preview-pane-100.png')
        self.button_view.setIcon(QIcon(file_path))


    def button_view_clicked(self):
        app.window_main_filler.view()


    def label_update(self):
        match self.code:
            case 0:
                label_name = {
                    0: 'Система в норме',
                    1: 'Выставте ttttку робота в нулевую позицию и нажмите продолжить',
                }
            case 1:
                label_name = {
                    0: 'Закончилась бутылка 2',
                    1: 'Началась rrrr калибровка робота (Подождите)',
                }
            case 2:
                label_name = {
                    0: 'Закончилась бутылка 2',
                    1: 'Поставьте rrrr стакан для розлива и нажмите стоп когда пойдет вода',
                }
            case 3:
                label_name = {
                    0: 'Поставьте стакан в рабочую область',
                    1: 'Система готова444. Нажмите продолжить',
                }
            case 4:
                pass
            case _:
                label_name = {
                    0: '',
                    1: '',
                }

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)

        self.label_3.setText(label_name[self.lang])


    def progressBar_1_update(self):
        pre_value = {
            0: 'мл', 
            1: 'ml', 
        }

        pre_value = pre_value[self.lang]

        self.progressBar_1.setFormat(f"%v {pre_value}")
        self.progressBar_1.setFont(QFont(app.font_family, 25))
        self.progressBar_1.setMinimum(0)
        self.progressBar_1.setMaximum(104)
        self.progressBar_1.setAlignment(Qt.AlignTop) 

        self.progressBar_1.setValue(36)
    

    def progressBar_2_update(self):
        pre_value = {
            0: 'мл', 
            1: 'ml', 
        }

        pre_value = pre_value[self.lang]

        self.progressBar_2.setFormat(f"%v {pre_value}")
        self.progressBar_2.setFont(QFont(app.font_family, 25))
        self.progressBar_2.setMinimum(0)
        self.progressBar_2.setMaximum(104)
        self.progressBar_2.setAlignment(Qt.AlignTop) 

        self.progressBar_2.setValue(36)


    def progressBar_recolor(self):
        stylesheet = app.styleSheet()
        
        if self.play == True:
            new_stylesheet = stylesheet.replace(
                'background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 rgb(200, 200, 200), stop: 0.6 rgb(128, 128, 128), stop: 0.8 rgb(80, 80, 80));',
                'background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 rgb(150, 210, 182), stop: 0.6 rgb(10, 158, 89), stop: 0.8 rgb(21, 130, 79));',
            )  
        else:
            new_stylesheet = stylesheet.replace(
                'background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 rgb(150, 210, 182), stop: 0.6 rgb(10, 158, 89), stop: 0.8 rgb(21, 130, 79));',
                'background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 rgb(200, 200, 200), stop: 0.6 rgb(128, 128, 128), stop: 0.8 rgb(80, 80, 80));'
            ) 

        
        app.setStyleSheet(new_stylesheet)
    

    def value_1_update(self):
        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(35)
        font.setBold(False)
        font.setWeight(50)

        self.value_1.setFont(font)

        pre_value = {
            0: 'мл', 
            1: 'ml', 
        }

        pre_value = pre_value[self.lang]

        value = 11

        self.value_1.setText(f'{value} {pre_value}')


    def value_2_update(self):
        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(35)
        font.setBold(False)
        font.setWeight(50)

        self.value_2.setFont(font)
        
        pre_value = {
            0: 'мл', 
            1: 'ml', 
        }

        pre_value = pre_value[self.lang]

        value = 12

        self.value_2.setText(f'{value} {pre_value}')

    
    def label_drink_1_update(self):
        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)

        self.label_drink_1.setFont(font)

        text = {
            0: 'Бутылка 1', 
            1: 'Drink 1', 
        }

        text = text[self.lang]

        self.label_drink_1.setText(f'{text}')


    def label_drink_2_update(self):
        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)

        self.label_drink_2.setFont(font)

        text = {
            0: 'Бутылка 2', 
            1: 'Drink 2', 
        }

        text = text[self.lang]

        self.label_drink_2.setText(f'{text}')

    
    def label_value_1_update(self):
        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(21)
        font.setBold(False)
        font.setWeight(50)

        self.label_value_1.setFont(font)

        text = {
            0: 'Дозировка 1', 
            1: 'Dosing 1', 
        }

        text = text[self.lang]

        self.label_value_1.setText(f'{text}')


    def label_value_2_update(self):
        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(21)
        font.setBold(False)
        font.setWeight(50)

        self.label_value_2.setFont(font)

        text = {
            0: 'Дозировка 2', 
            1: 'Dosing 2', 
        }

        text = text[self.lang]

        self.label_value_2.setText(f'{text}')


    
filler_window = filler_control()