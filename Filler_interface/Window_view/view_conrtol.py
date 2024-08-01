from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QImage, QPixmap
import os

from Filler_interface.app import app

try:
    from Filler_robot.robot_main import robot
    raspberry = True
except ImportError:
    raspberry = False


class View_control(QMainWindow):
    def __init__(self):
        super().__init__()

        file_path = os.path.join('Filler_interface', 'Window_view', 'UI_view.ui')
        uic.loadUi(file_path, self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.window_name = 'view'

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        file_path = os.path.join('Filler_interface', '1x', 'innotech_min.png')
        pixmap = QPixmap(file_path)
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.5), int(pixmap.height() * 0.5), Qt.KeepAspectRatio)
        self.innotech_min.setPixmap(scaled_pixmap)

        self.image_low()
        self.button_raise()

        self.focus_window = False

        self.frame_label = None

        if raspberry:
            robot.frame_captured.connect(self.update_frame)


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if raspberry:
            robot.neuron_on = True

        if app.on_fullscreen: self.fullscreen()

        self.update_label()

        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
        'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.4 #DCDCDC, stop: 0.9 #878787);',
        'background-color: None'
        )
        
        app.setStyleSheet(new_stylesheet)

        self.focus_window = True

        super().show()


    def close(self):
        if raspberry:
            robot.neuron_on = False

        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
        'background-color: None',
        'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.4 #DCDCDC, stop: 0.9 #878787);'
        )
        
        app.setStyleSheet(new_stylesheet)

        self.focus_window = False

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
        # file_path = os.path.join('Filler_interface', 'Window_view', 'images.png')
        # self.label.setPixmap(QPixmap(file_path))
        self.label.setScaledContents(True)
        self.label.lower()


    def update_frame(self, frame):
        self.frame_label = frame

        self.update_label()

        if self.focus_window:
            app.datetime_reset()


    def update_label(self):
        if self.frame_label is not None:
            h, w, ch = self.frame_label.shape
            q_image = QImage(self.frame_label.data.tobytes(), w, h, ch * w, QImage.Format_BGR888)

            pixmap = QPixmap.fromImage(q_image)
            self.label.setPixmap(pixmap)
        else:
            pass


        # pixmap = QPixmap(file_path)
        # #scaled_pixmap = pixmap.scaled(int(pixmap.width() * 2), int(pixmap.height() * 2), Qt.KeepAspectRatio)
        # self.label.setPixmap(pixmap)
    
    
window_view = View_control()