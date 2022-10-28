import sys
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QWidget, QStackedWidget, QWizard
from pyqt5_plugins.examplebutton import QtWidgets

colorChanged = pyqtSignal()


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('logo1.ui', self)
        self.colors = []
        self.btncolor.clicked.connect(self.choose_color)
        self.btnnext.clicked.connect(self.second_step)

    def choose_color(self):
        color_pallete = QColorDialog(self)
        if color_pallete.exec_():
            self.colors.append(color_pallete.currentColor().name())
            print(self.colors)

    def second_step(self):
        if self.lineEdit.text() == "":
            self.lineEdit.setPlaceholderText("*Обязательное поле для ввода")
        else:
            pass


class SecondPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic.loadUi('logo2.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPage()
    ex.show()
    sys.exit(app.exec_())
