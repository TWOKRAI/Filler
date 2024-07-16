from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from Window_datetime.datetime import Ui_MainWindow 
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QFont, QMovie
import datetime

from app import app


class GradientLabel(QLabel):
    def __init__(self, text, parent=None):
        super(GradientLabel, self).__init__(text, parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, Qt.red)
        gradient.setColorAt(1, Qt.blue)

        # Set pen
        painter.setPen(gradient)

        # Set font
        font = QFont('Arial', 200)
        painter.setFont(font)

        # Draw text
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class Datetime_control(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.update_time()

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.start_time = 500000

        pixmap = QPixmap('1x\innotech_min.png')
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.4), int(pixmap.height() * 0.4), Qt.KeepAspectRatio)
        self.innotech_min.setPixmap(scaled_pixmap)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        #self.timer.start(1000)
        
        self.time = GradientLabel('Hello, World!')

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


    def show_window(self):
        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
        'background-color: None',
        'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.5 #DCDCDC, stop: 0.9 #949494);'
        )
        
        app.setStyleSheet(new_stylesheet)
    
        self.timer.stop()
        self.timer.start(1000)

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
        self.timer.stop()
        app.window_main_filler.timer.stop()
        app.window_main_filler.timer.start()
        self.hide()


    def update_time(self):
        # font = QFont()
        # font.setFamily("Siemens AD Sans")
        # font.setPointSize(100)
        # self.time.setFont(font)

        now = datetime.datetime.now()
        time = now.strftime("%H:%M")
        date = now.strftime("%d/%m/%Y")
        # self.time.setText(time)
        self.date.setText(date)
    
    
window_datetime = Datetime_control()