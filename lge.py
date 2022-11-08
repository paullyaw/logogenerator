import sys
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QSize
import sqlite3
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog
from pyqt5_plugins.examplebutton import QtWidgets

colorChanged = pyqtSignal()
colors = []


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        im = QPixmap(f"images/pic/logo.png")
        self.logo.setPixmap(im.scaled(230, 100, 100))
        self.setWindowTitle("Генератор Логотипов")
        self.setWindowIcon(QIcon("images/pic/logoicon.ico"))
        self.window = InformationPage()
        self.pushButton.clicked.connect(lambda: self.show_window(self.window))

    def show_window(self, window):
        window.show()
        self.close()


class ColorPage(QMainWindow):
    def __init__(self):
        super().__init__()
        global colors
        color_pallete = QColorDialog(self)
        color_pallete.setStyleSheet("background-color: white;")

        if color_pallete.exec_():
            colors.append(color_pallete.currentColor().name())  # Добавление основных цветов в БД


class InformationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        global colors
        self.n = uic.loadUi('untitled1.ui', self)
        self.setWindowTitle("Генератор Логотипов")
        self.setWindowIcon(QIcon("images/pic/logoicon.ico"))

        self.db = sqlite3.connect("information.db")  # подключение БД
        self.cur = self.db.cursor()

        self.btncolor.clicked.connect(self.choose_color)  # Если пользователь нажал кнопку выбора цвета
        self.btnnext.clicked.connect(self.check_information)  # Если пользователь нажал кнопку "Дальше"

    def choose_color(self):
        ColorPage()

    def check_information(self):
        if self.lineEdit.text() == "":
            self.lineEdit.setPlaceholderText("*Обязательное поле для ввода")  # Проверка ввел ли пользователь название
            # бренда, для дальнейшей генерации
        elif not colors:
            self.btncolor.setStyleSheet('QPushButton {background: white; color: red}')  # Проверка выбрал ли
            # пользователь цвета
            self.btncolor.clicked.connect(self.change_btntext_color)
        if self.lineEdit.text() == "" and not colors:  # Проверка выбрал ли пользователь цвета и ввел название
            self.lineEdit.setPlaceholderText("*Обязательное поле для ввода")
            self.btncolor.setStyleSheet('QPushButton {background: white; color: red}')
            self.btncolor.clicked.connect(self.change_btntext_color)
        if self.lineEdit.text() != "" and colors:  # Добавление введенной информации в БД
            self.add_to_bd()
            self.window = GenerationPage()
            self.show_window(self.window)

    def change_btntext_color(self):
        self.btncolor.setStyleSheet('QPushButton {background: white; color: black}')  # Если пользователь выбрал
        # цвета, изменение цвета
        # текста кнопки

    def show_window(self, window):
        window.show()  # Показ слудующего окна
        self.close()

    def add_to_bd(self):
        nameBrand = self.lineEdit.text()
        aboutBrand = self.textEdit.toPlainText()
        sql = 'INSERT INTO inform (nameBrand, work, description, colors) VALUES (:nameBrand, "l", :aboutBrand, :colors)'
        self.cur.execute(sql, {"nameBrand": nameBrand, "aboutBrand": aboutBrand, "colors": ", ".join(colors)})
        self.db.commit()
        self.cur.close()  # Закрываем объект-курсор
        self.db.close()


class GenerationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled2.ui', self)
        self.setWindowTitle("Генератор Логотипов")
        self.setWindowIcon(QIcon("images/pic/logoicon.ico"))

        self.settings.setIcon(QIcon('images/pic/settings.png'))
        self.settings.setIconSize(QSize(40, 40))
        self.show()

        self.db = sqlite3.connect("logogenerator.db")  # подключение БД
        self.cur = self.db.cursor()

        self.window = FavoritesPage()
        self.btnfavorites.clicked.connect(lambda: self.show_window(self.window))

        self.window1 = ChangeInformation()
        self.settings.clicked.connect(lambda: self.show_window1(self.window1))

    def show_window(self, window):
        window.show()

    def show_window1(self, window1):
        window1.show()
        self.close()


class FavoritesPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled3.ui', self)
        self.setWindowTitle("Избранное")
        self.setWindowIcon(QIcon("images/pic/logoicon.ico"))


class ChangeInformation(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled1.ui', self)
        self.setWindowTitle("Изменение информации")
        self.setWindowIcon(QIcon("images/pic/logoicon.ico"))

        self.db = sqlite3.connect("information.db")  # подключение БД
        self.cur = self.db.cursor()
        information = """SELECT * from inform"""
        self.cur.execute(information)
        information = self.cur.fetchall()[-1]
        self.lineEdit.setText(information[1])
        self.textEdit.setText(information[3])
        self.btnnext.clicked.connect(self.close_event)

    def information(self):
        nameBrand = self.lineEdit.text()
        aboutBrand = self.textEdit.toPlainText()
        sql = 'UPDATE inform SET nameBrand = :nameBrand, description = :aboutBrand'
        self.cur.execute(sql, {"nameBrand": nameBrand, "aboutBrand": aboutBrand})
        self.db.commit()
        self.cur.close()  # Закрываем объект-курсор
        self.db.close()

    def close_event(self):
        result = QtWidgets.QMessageBox.question(self, "Подтверждение редактирования",
                                                "Вы действительно хотите изменить информацию?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            QtWidgets.QWidget.close(self)
            self.information()
            self.window = GenerationPage()
            self.show_window(self.window)

        else:
            QtWidgets.QWidget.close(self)
            self.window = GenerationPage()
            self.show_window(self.window)

    def show_window(self, window):
        window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPage()
    app.setStyle('Fusion')
    ex.show()
    sys.exit(app.exec_())
