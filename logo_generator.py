import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog

colorChanged = pyqtSignal()


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('logo1.ui', self)
        self.colors = []
        self.namebrand = ""
        self.aboutbrand = ""
        self.btncolor.clicked.connect(self.choose_color)  # Если пользователь нажал кнопку выбора цвета 
        self.btnnext.clicked.connect(self.check_information)  # Если пользователь нажал кнопку "Дальше"

    def choose_color(self):
        color_pallete = QColorDialog(self)
        if color_pallete.exec_():
            self.colors.append(color_pallete.currentColor().name())  # Добавление основных цветов в БД

    def check_information(self):
        if self.lineEdit.text() == "":
            self.lineEdit.setPlaceholderText("*Обязательное поле для ввода")  # Проверка ввел ли пользователь название
            # бренда, для дальнейшей генерации 
        elif not self.colors:
            self.btncolor.setStyleSheet('QPushButton {color: red}')  # Проверка выбрал ли пользователь цвета
            self.btncolor.clicked.connect(self.change_btntext_color)
        if self.lineEdit.text() == "" and not self.colors:  # Проверка выбрал ли пользователь цвета и ввел название
            self.lineEdit.setPlaceholderText("*Обязательное поле для ввода")
            self.btncolor.setStyleSheet('QPushButton {color: red}')
            self.btncolor.clicked.connect(self.change_btntext_color)
        if self.lineEdit.text() != "" and self.colors:  # Добавление введенной информации в БД 
            self.namebrand = self.lineEdit.text()
            if self.textEdit.toPlainText() != "":
                self.aboutbrand = self.textEdit.toPlainText()
            self.window = SecondPage()
            self.btnnext.clicked.connect(lambda: self.show_window(self.window))

    def change_btntext_color(self):
        self.btncolor.setStyleSheet('QPushButton {color: black}')  # Если пользователь выбрал цвета, изменение цвета 
        # текста кнопки 

    def show_window(self, window):
        window.show()  # Показ слудующего окна 


class SecondPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('logo2.ui', self)
        self.setWindowTitle("Генератор Логотипов")

        self.window = FavoritesPage()
        self.btnfavorites.clicked.connect(lambda: self.show_window(self.window))

    def show_window(self, window):
        window.show()  # Показ слудующего окна 


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

