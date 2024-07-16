from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from Window_view.view import Ui_MainWindow 
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QFont, QPixmap
import datetime

from app import app


class View_control(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        pixmap = QPixmap('1x\innotech_min.png')
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.4), int(pixmap.height() * 0.4), Qt.KeepAspectRatio)
        self.innotech_min.setPixmap(scaled_pixmap)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.label.setPixmap(QPixmap('Window_view\images.jpeg'))
        self.label.setScaledContents(True)
        self.label.lower()

        self.animation = QPropertyAnimation(self, b'windowOpacity')

        self.button = QPushButton(self)
        self.button.setObjectName("Button_close")
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.raise_()

        self.button.clicked.connect(self.close)


    def show_window(self):
        self.timer.stop()
        self.timer.start(300)

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
        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
        'background-color: None',
        'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.5 #DCDCDC, stop: 0.9 #949494);'
        )
        
        app.setStyleSheet(new_stylesheet)
        
        self.timer.stop()
        self.hide()



    def update_image(self):
        pixmap = QPixmap('Window_view\images.jpeg')
        #scaled_pixmap = pixmap.scaled(int(pixmap.width() * 2), int(pixmap.height() * 2), Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)

    
window_view = View_control()