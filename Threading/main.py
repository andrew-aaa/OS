import sys
import threading
from threading import Timer
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

import add


class Window(QMainWindow, add.App):
    def __init__(self):
        super().__init__()

        self.flag = True
        self.flag_thr = 0
        self.count = 0

        self.button_1 = QPushButton(self)
        self.button_1.setGeometry(QtCore.QRect(200, 10, 100, 40))
        self.button_1.setText("Start")
        self.button_1.clicked.connect(self.timerStart)
        self.button_2 = QPushButton(self)
        self.button_2.setGeometry(QtCore.QRect(200, 50, 100, 40))
        self.button_2.setText("Pause")
        self.button_2.clicked.connect(self.timerStop)
        self.button_3 = QPushButton(self)
        self.button_3.setGeometry(QtCore.QRect(200, 90, 100, 40))
        self.button_3.setText("Stop")
        self.button_3.clicked.connect(self.timerUpdate)
        self.button_4 = QPushButton(self)
        self.button_4.setGeometry(QtCore.QRect(320, 50, 100, 40))
        self.button_4.setText("Priority")
        self.button_4.clicked.connect(self.priority)

        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 10, 150, 50))
        self.label.setText("First thread timer")
        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 70, 150, 50))
        self.label.setText("Second thread timer")

        self.label_1 = QLabel(self)
        self.label_1.setGeometry(QtCore.QRect(160, 10, 50, 50))
        self.label_1.setText("")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(160, 70, 50, 50))
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)

    def timerStart(self):
        self.flag = True
        if self.flag_thr == 0 or self.flag_thr == 3:
            self.thread1 = threading.Thread(target=self.timer_1)
            self.thread2 = threading.Thread(target=self.timer_2, daemon=True)
        elif self.flag_thr == 1:
            self.thread1 = threading.Thread(target=self.timer_1)
        elif self.flag_thr == 2:
            self.thread2 = threading.Thread(target=self.timer_2, daemon=True)
        self.thread()

    def timerStop(self):
        self.flag = False

    def timerUpdate(self):
        self.flag = False
        self.count = 0
        if self.flag_thr == 0 or self.flag_thr == 3:
            self.label_1.setText("0")
            self.label_2.setText("0")
        elif self.flag_thr == 1:
            self.label_1.setText("0")
        elif self.flag_thr == 2:
            self.label_2.setText("0")

    def priority(self):
        if self.flag_thr == 3:
            self.flag_thr = 0
        self.flag_thr += 1

    def thread(self):
        if self.flag_thr == 0 or self.flag_thr == 3:
            self.thread1.start()
            self.thread2.start()
            self.thread1.join()
            self.thread2.join()
        elif self.flag_thr == 1:
            self.thread1.start()
            self.thread1.join()
        elif self.flag_thr == 2:
            self.thread2.start()
            self.thread2.join()

    def timer_1(self):
        if self.flag:
            self.label_1.setText(str(self.count))
            self.count += 1
            t = Timer(1.0, self.timer_1)
            t.start()


if __name__ == "__main__":
    Apper = QApplication(sys.argv)
    window = Window()
    window.resize(400, 150)
    window.show()
    sys.exit(Apper.exec_())
    sys.exit(0)
