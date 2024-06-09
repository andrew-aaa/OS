import sys
import os
import shutil
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication
from PyQt5.Qt import QTreeView, QInputDialog, QFileDialog, QFileSystemModel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.grid = QGridLayout(self)

        self.model = QFileSystemModel()
        self.model.setRootPath('')
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.grid.addWidget(self.tree, 111, 0, alignment=QtCore.Qt.AlignBottom)

        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.menu_f)

    def menu_f(self):
        menu = QtWidgets.QMenu()
        rename = menu.addAction("Rename")
        rename.triggered.connect(self.rename_file)
        remove = menu.addAction("Remove")
        remove.triggered.connect(self.remove_file)
        copy = menu.addAction("Copy")
        copy.triggered.connect(self.copy_file)
        move = menu.addAction("Move")
        move.triggered.connect(self.move_file)
        create = menu.addAction("Создать")
        create.triggered.connect(self.create_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def create_file(self):
        index = self.tree.currentIndex()
        file_name = self.model.filePath(index)
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter name:')
        if os.path.isdir(file_name):
            path = os.path.join(file_name, text)
            os.mkdir(path)
        else:
            direct = os.path.dirname(os.path.abspath(file_name))
            path = os.path.join(direct, text)
            os.mkdir(path)



    def remove_file(self):
        index = self.tree.currentIndex()
        file_name = self.model.filePath(index)
        if os.path.isdir(file_name):
            shutil.rmtree(file_name)
        else:
            os.remove(file_name)

    def copy_file(self):
        index = self.tree.currentIndex()
        file_name = self.model.filePath(index)
        if os.path.isdir(file_name):
            shutil.copytree(file_name, file_name + "_copy")
        else:
            basename, extension = os.path.splitext(file_name)
            shutil.copyfile(file_name, basename + "_copy" + extension)

    def rename_file(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Enter a new name:')
        index = self.tree.currentIndex()
        file_name = self.model.filePath(index)
        if ok:
            if os.path.isdir(file_name):
                direct = os.path.dirname(os.path.abspath(file_name))
                os.rename(file_name, direct + "/" + str(text))
            else:
                basename, extension = os.path.splitext(file_name)
                direct = os.path.dirname(os.path.abspath(file_name))
                os.rename(file_name, direct + "/" + str(text) + extension)

    def move_file(self):
        index = self.tree.currentIndex()
        file_name = self.model.filePath(index)
        direct = QFileDialog.getExistingDirectory(self, "Move file", file_name, QFileDialog.ShowDirsOnly)
        shutil.move(file_name, direct)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
