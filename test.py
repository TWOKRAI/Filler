import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import time

class Filler(QThread):
    update_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.count = 0
        self.running = False

    def run(self):
        while self.running:
            self.count += 1
            self.update_signal.emit(self.count)
            time.sleep(1)

    def starting(self):
        self.running = True
        self.start()

    def stop(self):
        self.running = False

    def go(self):
        print("go")

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.filler = Filler()
        self.filler.update_signal.connect(self.update_count)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt Example')

        self.count_label = QLabel('Count: 0', self)
        self.start_button = QPushButton('�����', self)
        self.stop_button = QPushButton('����', self)
        self.go_button = QPushButton('Go', self)

        self.start_button.clicked.connect(self.start_counting)
        self.stop_button.clicked.connect(self.stop_counting)
        self.go_button.clicked.connect(self.go)

        layout = QVBoxLayout()
        layout.addWidget(self.count_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.go_button)

        self.setLayout(layout)

    def start_counting(self):
        if not self.filler.isRunning():
            self.filler.starting()

    def stop_counting(self):
        self.filler.stop()

    def go(self):
        self.filler.go()
        print("go")

    def update_count(self, count):
        self.count_label.setText(f'Count: {count}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
