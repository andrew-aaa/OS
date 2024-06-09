import sys
from threading import Timer
from PyQt5.QtWidgets import *


class App(object):
    def ui(self, MainWindow):
        MainWindow.resize(50, 50)

        self.count = 0
        self.timer_2()

    def timer_2(self):
        if self.flag:
            self.label_2.setText(str(self.count))
            self.count += 1
            t = Timer(1.0, self.timer_2)
            t.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    window = App()
    window.ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
