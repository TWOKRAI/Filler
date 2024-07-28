from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import os

from Filler_interface.app import app


class View_control(QMainWindow):
    def __init__(self):
        super().__init__()

        file_path = os.path.join('Filler_interface', 'Window_view', 'UI_view.ui')
        uic.loadUi(file_path, self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        file_path = os.path.join('Filler_interface', '1x', 'innotech_min.png')
        pixmap = QPixmap(file_path)
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.5), int(pixmap.height() * 0.5), Qt.KeepAspectRatio)
        self.innotech_min.setPixmap(scaled_pixmap)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        self.image_low()
        self.button_raise()

        super().show()


    def show_window(self):
        if app.on_fullscreen: self.fullscreen()
        self.image_low()
        self.button_raise()

        self.timer.stop()
        self.timer.start(100)
        
        self.show()
        

    def close(self):
        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
        'background-color: None',
        'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.4 #DCDCDC, stop: 0.9 #878787);'
        )
        
        app.setStyleSheet(new_stylesheet)
        
        self.timer.stop()
        self.hide()


    def button_raise(self):
        self.button = QPushButton(self)
        self.button.setObjectName("Button_close")
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.raise_()

        self.button.clicked.connect(self.close)
    

    def image_low(self):
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width(), self.height())
        file_path = os.path.join('Filler_interface', 'Window_view', 'images.png')
        self.label.setPixmap(QPixmap(file_path))
        self.label.setScaledContents(True)
        self.label.lower()


    def update_image(self):
        file_path = os.path.join('Filler_interface', 'Window_view', 'images.jpg')
        pixmap = QPixmap(file_path)
        #scaled_pixmap = pixmap.scaled(int(pixmap.width() * 2), int(pixmap.height() * 2), Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)

    
window_view = View_control()