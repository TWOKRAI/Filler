from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton
from Window_main.main_filler import Ui_MainWindow 
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation
from PyQt5.QtGui import QIcon

from app import app


class Main_filler_control(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.timer = QTimer()
        self.timer.timeout.connect(self.datetime)
        
        icon_size = QSize(40, 40)

        self.start_text = [' Начать', ' Start', ' Beginnen', ' 開始']
        self.button_start.setIcon(QIcon('Style_windows\icons_black\icons8-wine-bar-100.png'))
        self.button_start.setIconSize(icon_size)

        self.button_start.clicked.connect(self.start)


        self.game_text = [' Игры', ' Games', ' Spiele', ' 遊戲']
        self.button_game.setIcon(QIcon('Style_windows\icons_black\icons8-game-controller-100.png'))
        self.button_game.setIconSize(icon_size)

        self.button_game.clicked.connect(self.game)


        self.settings_text = [' Настройки', ' Settings', ' Einstellungen', ' 設定']
        self.button_settings.setIcon(QIcon('Style_windows\icons_black\icons8-automation-100.png'))
        self.button_settings.setIconSize(icon_size)

        self.button_settings.clicked.connect(self.settings)


        self.view_text = [' Вид', ' View', ' Sicht', ' 看法']
        self.button_view.setIcon(QIcon('Style_windows\icons_black\icons8-глаз-100.png'))
        self.button_view.setIconSize(icon_size)

        self.button_view.clicked.connect(self.view)


        self.statistics_text = [' Статистика', ' Statistics', ' Statistiken', ' 統計數據']
        self.button_statistics.setIcon(QIcon('Style_windows\icons_black\icons8-статистика-100.png'))
        self.button_statistics.setIconSize(icon_size)

        self.button_statistics.clicked.connect(self.statistics)

        self.animation = QPropertyAnimation(self, b'windowOpacity')


    def show_window(self):
        self.timer.stop()
        self.timer.start(app.window_datetime.start_time)

        self.setWindowOpacity(0.0)  
        self.show()  
        self.start_animation()


    def start_animation(self):
        self.animation.stop()
        self.animation.setDuration(2000)  
        self.animation.setStartValue(0.0)  
        self.animation.setEndValue(1.0) 
        self.animation.start()


    def language(self, lang):
        self.button_start.setText(self.start_text[lang])
        self.button_settings.setText(self.settings_text[lang])
        self.button_view.setText(self.view_text[lang])
        self.button_game.setText(self.game_text[lang])
        self.button_statistics.setText(self.statistics_text[lang])
    

    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def start(self):
        app.window_settings1.param_num = 0

        app.window_settings1.update()
        
        app.window_settings1.show()
        self.hide()

    
    def datetime(self):
        app.window_datetime.show_window()
        self.timer.stop()


    def game(self):
        app.exit()
    

    def settings(self):
        app.window_settings2.show()
        self.hide()

    
    def view(self):
        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
            'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.5 #DCDCDC, stop: 0.9 #949494);',
            'background-color: None'
        )
        
        app.setStyleSheet(new_stylesheet)
        app.window_view.show()

    
    def statistics(self):
        pass



main_filler_window = Main_filler_control()
