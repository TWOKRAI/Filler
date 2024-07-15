from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from app import app


class Pop_up_control(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Window_pop_up/UI_pop_up.ui', self)
       
        self.statusBar().setHidden(True)

        self.setWindowFlags(Qt.FramelessWindowHint) 
        self.setWindowFlag(Qt.FramelessWindowHint, True)

        self.func = None

        self.font_text = QFont()
        self.font_text.setFamily("Siemens AD Sans")

        font_1 = QFont()
        font_1.setFamily("Siemens AD Sans")
        font_1.setPointSize(22)
        font_1.setBold(False)
        font_1.setWeight(50)

        font_2 = QFont()
        font_2.setFamily("Siemens AD Sans")
        font_2.setPointSize(14)
        font_2.setBold(False)
        font_2.setWeight(50)

        self.label_2.setFont(font_1)
        self.label_2.setWordWrap(True)

        self.pushButton_ok.setFixedSize(150, 100)
        self.pushButton_ok.setFont(font_2)

        self.pushButton_ok.clicked.connect(self.ok)


        self.pushButton_cancel.setFixedSize(150, 100)
        self.pushButton_cancel.setFont(font_2)

        self.pushButton_cancel.clicked.connect(self.cancel)

        self.setStyleSheet("""
            QWidget{
                border: 3px solid rgb(108, 161, 141);
            }
            
            QLabel{
                border: 0px solid rgb(108, 161, 141);        
            }
                           
            QPushButton {
                background-color: #dad7d7;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                stop: 0 white, stop: 0.7 #A9A9A9, stop: 0.95 #dad7d7);
                border-radius: 25px;
                color: rgb(63, 94, 83);
                border: 4px solid rgb(108, 161, 141);
                border-bottom: 5px solid rgb(87, 121, 101);
            }

            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, 
                stop: 0 white, stop: 0.7 #A9A9A9, stop: 0.95 #dad7d7);
                border: 4px solid rgb(108, 161, 141);
            }

            QPushButton#Button_close {
                background-color: rgba(0, 0, 0, 0);
                border: none;
            }
        """)

        self.lang = 0

        self.text = [
            'Вы хотите сделать сброс параметров?', 
            'Volume1 /ml',
            'Volumen 1 /ml', 
            '體積 1 /毫升',
        ]

        self.text_button_ok = [
            'ПОДТВЕРДИТЬ', 
            'Volume1 /ml',
            'Volumen 1 /ml', 
            '體積 1 /毫升',
        ]

        self.text_button_cancel = [
            'ОТМЕНИТЬ', 
            'Volume1 /ml',
            'Volumen 1 /ml', 
            '體積 1 /毫升',
        ]

        self.font_size = [
            [22, 14],
            [22, 14],
            [22, 14],
            [22, 14],
        ]


    def show(self, func):
        if app.on_fullscreen: self.fullscreen()
        self.update_text()
        self.func = func

        super().show()


    def language(self, lang):
        self.lang = lang

        self.update_text()


    def update_text(self):
        size = self.font_size[self.lang][0]
        self.font_text.setPointSize(size)
        self.label_2.setFont(self.font_text)
        self.label_2.setText(self.text[self.lang])

        size = self.font_size[self.lang][1]
        self.font_text.setPointSize(size)
        self.pushButton_ok.setFont(self.font_text)
        self.pushButton_ok.setText(self.text_button_ok[self.lang])

        size = self.font_size[self.lang][1]
        self.font_text.setPointSize(size)
        self.pushButton_cancel.setFont(self.font_text)
        self.pushButton_cancel.setText(self.text_button_cancel[self.lang])


    def ok(self):
        self.func()
        self.hide()

    
    def cancel(self):
        self.hide()
        

window_pop_up = Pop_up_control()