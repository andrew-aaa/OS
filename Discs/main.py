import win32api
import psutil
from threading import Timer
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(620, 200)
        MainWindow.setStyleSheet("background-color: rgb(41, 49, 51);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 620, 135))
        self.tableWidget.setStyleSheet("background-color: rgb(71, 74, 81);")
        self.tableWidget.setObjectName("tableWidget")
        self.table()

        self.Button = QtWidgets.QPushButton(self.centralwidget)
        self.Button.setGeometry(QtCore.QRect(500, 150, 100, 50))
        self.Button.setStyleSheet("background: rgb(255, 255, 0);")
        self.Button.setText("Завершить")
        self.Button.clicked.connect(lambda: self.stop())


        MainWindow.setCentralWidget(self.centralwidget)

    def table(self):
        Timer(1, self.table).start()
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(len(drives))
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Type", "Total", "Used", "Free", "%"])

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 170, 381, 31))
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setText("RAM: total-{0}GB; used-{1}GB; free-{2}GB {3}%".format(round(psutil.virtual_memory()[0]/10**9, 3),
                                                                          round(psutil.virtual_memory()[3]/10**9, 3),
                                                                          round(psutil.virtual_memory()[4]/10**9, 3),
                                                                          psutil.virtual_memory()[2]))
        self.label.setObjectName("label")



        disk_part = psutil.disk_partitions(all=True)

        for i in range(len(drives)):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(drives[i]))
            disk_info = psutil.disk_usage(drives[i])
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(disk_info.total / 2 ** 30)[:7]))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(disk_info.used / 2 ** 30)[:7]))
            self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(str(disk_info.free / 2 ** 30)[:7]))
            self.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(str(disk_info.percent)))

        c = 0
        for disk_p in disk_part:
            self.tableWidget.setItem(c, 1, QtWidgets.QTableWidgetItem(disk_p.fstype))
            c += 1

    def stop(self):
        Timer.cancel()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    Ui_MainWindow.stop()

