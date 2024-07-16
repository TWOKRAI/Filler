from PyQt5.QtWidgets import QMainWindow, QPushButton
from Window_start.start import Ui_MainWindow 
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QPixmap

from app import app


class Start_control(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        pixmap = QPixmap('1x\innotech_max_2.png')
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.8), int(pixmap.height() * 0.8), Qt.KeepAspectRatio)
        self.innotech.setPixmap(scaled_pixmap)

        self.timer = QTimer()
        self.timer.timeout.connect(self.close_auto)
        self.timer.start(5000)

        self.button = QPushButton(self)
        self.button.setObjectName("Button_close")
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.raise_()

        self.animation = QPropertyAnimation(self, b'windowOpacity')

        self.button.clicked.connect(self.close)
    

    def show_window(self):
        self.setWindowOpacity(0.0)  # Устанавливаем начальную прозрачность на 0,0
        self.show()  # Отображаем окно
        self.start_animation()


    def start_animation(self):
        self.animation.stop()
        self.animation.setDuration(2000)  # Длительность в миллисекундах
        self.animation.setStartValue(0.0)  # Начальная прозрачность
        self.animation.setEndValue(1.0)  # Конечная прозрачность
        self.animation.start()


    def close(self):
        self.timer.stop()
        app.window_main_filler.show()
        app.window_main_filler.timer.start(30000)
        self.hide()
    

    def close_auto(self):
        self.timer.stop()
        app.window_main_filler.show_window()

        QTimer.singleShot(3000, self.hide)
    
    

window_start = Start_control()