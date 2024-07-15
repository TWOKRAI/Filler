from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation
from PyQt5.QtGui import QIcon, QFont

from app import app


class Control(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Window_list1/UI.ui', self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.timer = QTimer()
        self.timer.timeout.connect(self.datetime)
        
        icon_size = QSize(50, 50)
        icon_size_2 = QSize(60, 60)
        button_size = QSize(200, 120)
        button_size_2 = QSize(130, 120)

        font = QFont()
        font.setFamily("Siemens AD Sans")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)


        self.button_menu.setMinimumSize(button_size_2)
        self.button_menu.setIconSize(icon_size_2)

        self.button_menu.clicked.connect(self.button_menu_clicked)


        self.start_text = [' Начать', ' Start', ' Beginnen', ' 開始']
        
        self.button_start.setMinimumSize(button_size)
        self.button_start.setIconSize(icon_size)
        self.button_start.setFont(font)

        self.button_start.clicked.connect(self.start)


        self.game_text = [' Игры', ' Games', ' Spiele', ' 遊戲']
        
        self.button_game.setMinimumSize(button_size)
        self.button_game.setIconSize(icon_size)
        self.button_game.setFont(font)

        self.button_game.clicked.connect(self.game)


        self.statistics_text = [' Статистика', ' Statistics', ' Statistiken', ' 統計數據']
        
        self.button_statistics.setMinimumSize(button_size)
        self.button_statistics.setIconSize(icon_size)
        self.button_statistics.setFont(font)

        self.button_statistics.clicked.connect(self.statistics)

        self.animation = QPropertyAnimation(self, b'windowOpacity')

        self.set_icons()


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()

        #self.language(app.lang)
        super().show()


    def set_icons(self):
        self.button_menu.setIcon(QIcon(f'Style_windows/icons_black/icons8-menu-100.png'))
        self.button_start.setIcon(QIcon('Style_windows\icons_black\icons8-wine-bar-100.png'))
        self.button_game.setIcon(QIcon('Style_windows\icons_black\icons8-game-controller-100.png'))
        self.button_statistics.setIcon(QIcon('Style_windows\icons_black\icons8-pie-chart-100.png'))


    def language(self, lang):
        self.button_start.setText(self.start_text[lang])
        self.button_game.setText(self.game_text[lang])
        self.button_statistics.setText(self.statistics_text[lang])
    

    def button_menu_clicked(self):
        app.window_main_filler.show()
        self.hide()


    def start(self):
        app.window_settings1.param_num = 1

        app.window_settings1.update()
        
        app.window_settings1.show()
        self.hide()

    
    def datetime(self):
        app.window_datetime.show_window()
        self.timer.stop()


    def game(self):
        app.check_timer()
        pass
    

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
        app.window_statistic.show()
        self.hide()


window_list1 = Control()
