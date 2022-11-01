import sys
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QWidget, QStackedWidget, QWizard, QMessageBox
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
        elif not self.colors:
            self.btncolor.setStyleSheet('QPushButton {color: red}')
            self.btncolor.clicked.connect(self.change_btntext_color)
        else:
            self.window = SecondPage()
            self.btnnext.clicked.connect(lambda: self.show_window(self.window))

    def change_btntext_color(self):
        self.btncolor.setStyleSheet('QPushButton {color: black}')

    def show_window(self, window):
        window.show()


class SecondPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('logo2.ui', self)
        self.setWindowTitle("Генератор Логотипов")

        self.window = FavoritesPage()
        self.btnfavorites.clicked.connect(lambda: self.show_window(self.window))

    def show_window(self, window):
        window.show()


class FavoritesPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('logo3.ui', self)
        self.setWindowTitle("Избранное")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPage()
    ex.show()
    sys.exit(app.exec_())
