from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import os

from Filler_interface.app import app


class Prepare_control(QMainWindow):
    calibration = pyqtSignal()
    reset_calibration = pyqtSignal()
    find_cup = pyqtSignal()
    pumping = pyqtSignal()
    stop_pumping = pyqtSignal()
    start_filler = pyqtSignal()

    def __init__(self):
        super().__init__()

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Window_prepare', 'UI_prepare.ui')
        # file_path = os.path.join('Filler_interface', 'Window_prepare', 'UI_prepare.ui')
        uic.loadUi(file_path, self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.window_name = 'prepare'

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

        self.update_text()

        app.window_focus = self.window_name
        print(app.window_focus)
        app.close_windows()

        # app.threads.start_robot_thread(camera_on = True, neuron_on = True, interface_on = True, robot_on = True)


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
        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-replay-100.png')
        self.button_reset.setIcon(QIcon(file_path))


    def reset(self):
        self.param_num = 0
        
        self.value = 0
        self.myprogressBar.setValue(self.value)
        self.button_calibr.setEnabled(True)

        app.threads.robot_filler.calibration_stop()

        self.reset_calibration.emit()

        self.update_text()
        

    def button_menu_update(self):
        icon_size = QSize(60, 60)
        self.button_menu.setIconSize(icon_size)

        button_size = QSize(130, 120)
        self.button_menu.setFixedSize(button_size)

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-menu-100.png')
        self.button_menu.setIcon(QIcon(file_path))


    def button_menu_clicked(self):
        app.threads.robot_filler.calibration_stop()
        app.window_main_filler.show()
        self.hide()


    def button_menu_pressed(self):
        self.timer.start()


    def button_menu_released(self):
        self.timer.stop()
 
        
    def on_timer_timeout(self):
        app.threads.robot_filler.calibration_stop()

        app.window_main_filler.show()
        self.hide()
    

    def button_calibr_update(self):
        match self.param_num:
            case 0:
                name_button = {
                    0: 'КАЛИБРОВКА',
                    1: 'Start1',
                }

            case 1:
                name_button = {
                    0: 'ПОДОЖДИТЕ',
                    1: '',
                }


            case 2:
                name_button = {
                    0: 'ПОДОЖДИТЕ',
                    1: 'Start2',
                }


            case 3:
                name_button = {
                    0: 'ПОДОЖДИТЕ',
                    1: 'Start2',
                }

  
            case 4:
                name_button = {
                    0: 'Готово',
                    1: 'Start2',
                }


            case 6:
                name_button = {
                    0: 'Начать',
                    1: 'Start2',
                }


            case _:
                name_button = {
                    0: 'Начать',
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

        print('self.param_num', self.param_num)

        if app.threads.robot_filler.robot.calibration_ready == True:
            self.param_num = 5
            app.threads.robot_filler.robot.calibration_ready = False

        match self.param_num:
            case 1:
                app.threads.robot_filler.calibration_run()

                self.value = 25

                self.button_calibr.setEnabled(False)
            
            case 2:                
                self.value = 50

            case 3:
                self.value = 70

            case 4:
                self.value = 90
        
            case 5:
                self.value = 100

                app.threads.robot_filler.calibration_stop()
            case 6:
                app.threads.robot_filler.filler_run()

                app.threads.robot_filler.robot.calibration_ready = True

                app.window_filler.show()
                self.hide()
                # self.param_num = 0

            case _:
                pass
        

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
                    0: 'Поставьте стакан перед роботом и нажмите "Калибровка"',
                    1: 'Выставте ttttку робота в нулевую позицию и нажмите продолжить',
                }



            case 1:
                label_name = {
                    0: 'Началась калибровка робота',
                    1: 'Началась rrrr калибровка робота ',
                }

      


            case 2:
                label_name = {
                    0: 'Поставьте стакан в рабочую зону для прокачки системы',
                    1: 'Поставьте стакан в рабочую зону для прокачки системы',
                }
                                
   

            case 3:
                label_name = {
                    0: 'Стакан обнаружен, началась прокачка системы',
                    1: 'Началась rrrr калибровка робота (Подождите)',
                }


            case 4:
                label_name = {
                    0: 'Прокачка системы закончена',
                    1: 'Поставьте rrrr стакан для розлива и нажмите стоп когда пойдет вода',
                }
                                

                self.value = 90

            case 5:
                label_name = {
                    0: 'Прокачка закончена',
                    1: 'Началась rrrr калибровка робота (Подождите)',
                }

                self.label.setText(label_name[self.lang])
                self.button_calibr.setEnabled(True)

                self.label.setText(label_name[self.lang])

                self.value = 100
            case 6:
                label_name = {
                    0: '',
                    1: '',
                }
            case _:
                pass


        self.label.setText(label_name[self.lang])
        

    def update_prepare(self, id):
        print('id', id)

        match id:
            case 0:
                label_name = {
                    0: 'Калибровка готова (Нажмите продолжить)',
                    1: 'Началась rrrr калибровка робота (Подождите)',
                }

                self.label.setText(label_name[self.lang])
                self.button_calibr.setEnabled(True)

                self.value = 40

                self.myprogressBar.setValue(self.value)

                print(self.value)


            case 1:
                label_name = {
                    0: 'Стакан обнаружен (Нажмите Прокачка)',
                    1: 'Началась rrrr калибровка робота (Подождите)',
                }

                self.label.setText(label_name[self.lang])
                self.button_calibr.setEnabled(True)

                self.value = 65

                self.myprogressBar.setValue(self.value)

                print(self.value)
                
            case 2:
                label_name = {
                    0: 'Система готова (Нажмите Начать)',
                    1: 'Началась rrrr калибровка робота (Подождите)',
                }

                self.label.setText(label_name[self.lang])
                self.button_calibr.setEnabled(True)

                self.value = 100

                self.myprogressBar.setValue(self.value)

                print(self.value)
            
        


window_prepare = Prepare_control()
