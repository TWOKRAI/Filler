from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from Window_level.level import Ui_MainWindow 
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QFont, QMovie
import datetime

from app import app


class level_control(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.start_time = 5000

        pixmap = QPixmap('1x\innotech_min.png')
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.4), int(pixmap.height() * 0.4), Qt.KeepAspectRatio)
        self.innotech_min.setPixmap(scaled_pixmap)

        pixmap = QPixmap('Style_windows\level\level_2.png')
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.7), int(pixmap.height() * 0.7), Qt.KeepAspectRatio)
        self.level_img.setPixmap(scaled_pixmap)


        self.button = QPushButton(self)
        self.button.setObjectName("Button_close")
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.raise_()

        self.animation = QPropertyAnimation(self, b'windowOpacity')

        self.button.clicked.connect(self.close)
        
        movie = QMovie("path/to/your/gif/file.gif")
        movie.setScaledSize(QSize(self.width(), self.height()))

        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.label.setMovie(movie)
        movie.start()


    def timing(self):
        self.timer.stop()


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show_window(self):
        if app.on_fullscreen: self.fullscreen()

        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
        'background-color: None',
        'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.5 #DCDCDC, stop: 0.9 #949494);'
        )
        
        app.setStyleSheet(new_stylesheet)

        self.setWindowOpacity(0.0)  
        self.show()  
        self.start_animation()


    def start_animation(self):
        self.animation.stop()
        self.animation.setDuration(2000)  
        self.animation.setStartValue(0.0)  
        self.animation.setEndValue(1.0) 
        self.animation.start()
    

    def close(self):
        self.hide()

    
window_level = level_control()