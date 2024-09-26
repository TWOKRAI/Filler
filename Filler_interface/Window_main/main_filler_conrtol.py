from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont
import os

from Filler_interface.app import app, enable_marker_decorator


class Main_filler_control(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window_name = 'main_filler'

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Window_main', 'UI_main_filler.ui')
        # file_path = os.path.join('Filler_interface', 'Window_main', 'UI_main_filler.ui')
        uic.loadUi(file_path, self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        icon_size = QSize(50, 50)
        button_size = QSize(210, 130)

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        

        self.start_text = ['НАЧАТЬ', 'START', 'STARTEN']
        self.button_start.setMinimumSize(button_size)
        self.button_start.setMaximumSize(button_size)
        self.button_start.setIconSize(QSize(55, 55))
        
        font1 = QFont()
        font1.setFamily(app.font_family)
        font1.setPointSize(18)
        font1.setBold(False)
        font1.setWeight(50)
        self.button_start.setFont(font1)
        
        #self.button_start.clicked.connect(self.start)
        self.button_start.released.connect(self.start)
        

        self.game_text = [' РОБОТ', ' ROBOT', ' ROBOTER']
        self.button_robot.setMinimumSize(button_size)
        self.button_robot.setMaximumSize(button_size)
        self.button_robot.setIconSize(icon_size)
        self.button_robot.setFont(font)

        #self.button_robot.clicked.connect(self.robot)
        self.button_robot.released.connect(self.robot)


        self.settings_text = [' НАСТРОЙКИ', ' SETTINGS', 'EINSTELLUNGEN']
        self.button_settings.setMinimumSize(button_size)
        self.button_settings.setMaximumSize(button_size)
        self.button_settings.setIconSize(icon_size)
        self.button_settings.setFont(font)

        #self.button_settings.clicked.connect(self.settings)
        self.button_settings.released.connect(self.settings)


        self.view_text = [' ВИД', ' VISION', ' VISION']
        self.button_view.setMinimumSize(button_size)
        self.button_view.setMaximumSize(button_size)
        self.button_view.setIconSize(QSize(55, 55))
        self.button_view.setFont(font)

        #self.button_view.clicked.connect(self.view)
        self.button_view.released.connect(self.view)


        self.statistics_text = [' ПРОМЫВКА', ' RINSE', ' SPÜLEN']
        self.button_cip.setMinimumSize(button_size)
        self.button_cip.setIconSize(icon_size)
        self.button_cip.setFont(font)

        #self.button_cip.clicked.connect(self.cip)
        self.button_cip.released.connect(self.cip)

        self.set_icons()

        self.timer_enable = QTimer(self)
        self.timer_enable.setSingleShot(True)  
        self.timer_enable.timeout.connect(self.all_enable_on)
        self.timer_enable.start(1000) 
        self.enable_marker = True


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        
        super().show()

        app.window_focus = self.window_name
        print(app.window_focus)
        #app.close_windows()

        self.setFocus()

        QTimer.singleShot(1000, self.no_focus_button)

        self.all_enable_off()


    def show_animation(self):
        if app.on_fullscreen: self.fullscreen()
        self.show()


    def language(self, lang):
        self.button_start.setText(self.start_text[lang])
        self.button_settings.setText(self.settings_text[lang])
        self.button_view.setText(self.view_text[lang])
        self.button_robot.setText(self.game_text[lang])
        self.button_cip.setText(self.statistics_text[lang])
    
    
    def set_icons(self):
        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-wine-bar-100.png')
        self.button_start.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-robotic-arm-100.png')
        self.button_robot.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-automation-100.png')
        self.button_settings.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-preview-pane-100.png')
        self.button_view.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-водяной-шланг-100.png')
        self.button_cip.setIcon(QIcon(file_path))

    
    def no_focus_button(self): 
        self.button_start.setDown(False)
        self.button_robot.setDown(False)
        self.button_settings.setDown(False)
        self.button_view.setDown(False)
        self.button_cip.setDown(False)

        self.button_start.clearFocus()
        self.button_robot.clearFocus()
        self.button_settings.clearFocus()
        self.button_view.clearFocus()
        self.button_cip.clearFocus()

        print('NO FOCUS')

    
    def all_enable_on(self):
        self.enable_marker = True

    
    def all_enable_off(self):
        self.enable_marker = False
        self.timer_enable.start()


    @enable_marker_decorator('enable_marker')
    def start(self):
        app.window_prepare.hide()
        app.window_prepare.show()
        #self.setFocus()
        #self.hide()
        

    @enable_marker_decorator('enable_marker')
    def robot(self):
        app.window_robot.hide()
        app.window_robot.show()
        #self.setFocus()
        #self.hide()
    

    @enable_marker_decorator('enable_marker')
    def settings(self):
        app.window_settings2.hide()
        app.window_settings2.show()
        self.setFocus()
        #self.hide()
       
    
    @enable_marker_decorator('enable_marker')
    def view(self):
        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
            'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.4 #DCDCDC, stop: 0.9 #878787);',
            'background-color: None'
        )
        
        app.setStyleSheet(new_stylesheet)
        app.window_view.show(1)

        self.setFocus()
        
        #self.hide()


    @enable_marker_decorator('enable_marker')
    def cip(self):
        app.window_cip.hide()
        app.window_cip.show()
        self.setFocus()
        #self.hide()


main_filler_window = Main_filler_control()
