import sys
from PyQt5 import uic, QtGui
from PyQt5.QtCore import pyqtSignal, QSize, Qt
import sqlite3
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QWidget
from PyQt5 import QtWidgets
from random import choice
from PIL import ImageColor

colorChanged = pyqtSignal()
colors = []
color_now1 = []
color_now2 = []
color_now3 = []
fonts = ["Muller ExtraBold", "Muller ExtraBold Italic", "Muller Medium", "Muller Medium Italic", "Novartis",
         "EV_Hater"]
color_now = ""
text = ""
flag = False


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        im = QPixmap(f"images/pic/logo.png")
        self.logo.setPixmap(im.scaled(230, 100, 100))  # изменение размера картинки-логотипа
        self.setWindowTitle("Генератор Логотипов")  # заголовок окна
        self.setWindowIcon(QIcon("images/pic/logoicon.ico"))  # установление иконки
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint) # 
        # убирается возможность масштабировать окно
        self.window = InformationPage()
        self.pushButton.clicked.connect(lambda: self.show_window(self.window))

    def show_window(self, window):
        window.show()  # переход на следующее окно
        self.close()  # закрытие нынешнего окна


class ColorPage(QMainWindow):
    def __init__(self):
        super().__init__()
        global colors, color_now
        color_pallete = QColorDialog.getColor()  # открытие диалогового окна выбора цвета
        if color_pallete.isValid():  # проверка выбран ли цвет
            color_now = color_pallete.name()
            colors.append(color_pallete.name())  # Добавление основных цветов в БД


class InformationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        global colors, color_now, color_now1, color_now2, color_now3
        self.n = uic.loadUi('untitled1.ui', self)
        self.setWindowTitle("Генератор Логотипов")
        self.lineEdit.setFont(QtGui.QFont("Muller Medium", 10))
        self.textEdit.setFont(QtGui.QFont("Muller Medium", 10))
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon("images/pic/logoicon.ico"))

        self.db = sqlite3.connect("information.db")  # подключение БД
        self.cur = self.db.cursor()

        self.btncolor1.clicked.connect(self.choose_color)  # Если пользователь нажал кнопку выбора цвета
        self.btncolor2.clicked.connect(self.choose_color1)  # Если пользователь нажал кнопку выбора цвета
        self.btncolor3.clicked.connect(self.choose_color2)  # Если пользователь нажал кнопку выбора цвета
        self.btnnext.clicked.connect(self.check_information)  # Если пользователь нажал кнопку "Дальше"

    def choose_color(self):
        ColorPage()
        self.btncolor1.setStyleSheet(
            "background-color: {}".format(color_now))  # устанавливаетсязадний фон кнопки выбранным цветом
        color_now1.insert(0, color_now)

    def choose_color1(self):
        ColorPage()
        self.btncolor2.setStyleSheet(
            "background-color: {}".format(color_now))  # устанавливаетсязадний фон кнопки выбранным цветом
        color_now2.insert(0, color_now)

    def choose_color2(self):
        ColorPage()
        self.btncolor3.setStyleSheet(
            "background-color: {}".format(color_now))  # устанавливаетсязадний фон кнопки выбранным цветом
        color_now3.insert(0, color_now)

    def check_information(self):
        if self.lineEdit.text() == "":
            self.lineEdit.setPlaceholderText("*Обязательное поле для ввода")  # Проверка ввел ли пользователь название
            # бренда, для дальнейшей генерации
        elif not colors:
            self.btncolor1.setStyleSheet('QPushButton {background: red;}')  # Проверка выбрал ли
            # пользователь цвета
            self.btncolor2.setStyleSheet('QPushButton {background: red;}')
            self.btncolor2.setStyleSheet('QPushButton {background: red;}')
            self.btncolor.clicked.connect(self.change_btntext_color)
        if self.lineEdit.text() == "" and not colors:  # Проверка выбрал ли пользователь цвета и ввел название
            self.lineEdit.setPlaceholderText("*Обязательное поле для ввода")
            self.btncolor1.setStyleSheet('QPushButton {background: red;}')
            self.btncolor2.setStyleSheet('QPushButton {background: red;}')
            self.btncolor3.setStyleSheet('QPushButton {background: red;}')
        if self.lineEdit.text() != "" and colors:  # Добавление введенной информации в БД
            self.add_to_bd()
            self.window = GenerationPage()
            self.show_window(self.window)

    def show_window(self, window):
        window.show()  # Показ слудующего окна
        self.close()

    def add_to_bd(self):
        nameBrand = self.lineEdit.text()
        aboutBrand = self.textEdit.toPlainText()
        sql = 'INSERT INTO inform (nameBrand, work, description, colors) VALUES (:nameBrand, "l", :aboutBrand, :colors)'
        # добавление в базу данных
        self.cur.execute(sql, {"nameBrand": nameBrand, "aboutBrand": aboutBrand, "colors": ", ".join(colors)})
        self.db.commit()
        self.cur.close()  # Закрываем объект-курсор
        self.db.close()


class GenerationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        global fonts, text, flag, pixmap
        uic.loadUi('untitled2.ui', self)
        self.setWindowTitle("Генератор Логотипов")
        self.setWindowIcon(QIcon("images/pic/logoicon.ico"))
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.settings.setIcon(QIcon('images/pic/settings.png'))
        self.settings.setIconSize(QSize(40, 40))
        self.show()

        self.db = sqlite3.connect("information.db")  # подключение БД
        self.cur = self.db.cursor()
        information = """SELECT * from inform"""
        # получение информации из БД
        self.cur.execute(information)
        information = self.cur.fetchall()[-1]
        text = information[1]
        self.window2 = Example()
        self.btnge.clicked.connect(lambda: self.show_window2(self.window2))

        self.window1 = ChangeInformation()
        self.settings.clicked.connect(lambda: self.show_window1(self.window1))

    def show_window(self, window):
        window.show()

    def show_window1(self, window1):
        window1.show()
        self.close()

    def show_window2(self, window2):
        window2.show()


class ChangeInformation(QMainWindow):
    def __init__(self):
        super().__init__()
        global colors, color_now, color_now1, color_now2, color_now3
        uic.loadUi('untitled1.ui', self)
        self.setWindowTitle("Изменение информации")
        self.setWindowIcon(QIcon("images/pic/logoicon.ico"))
        self.lineEdit.setFont(QtGui.QFont("Muller Medium", 10))
        self.textEdit.setFont(QtGui.QFont("Muller Medium", 10))
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.btncolor1.clicked.connect(self.choose_color)
        self.btncolor2.clicked.connect(self.choose_color1)
        self.btncolor3.clicked.connect(self.choose_color2)
        self.db = sqlite3.connect("information.db")  # подключение БД
        self.cur = self.db.cursor()
        information = """SELECT * from inform"""
        # получение информации из БД
        self.cur.execute(information)
        information = self.cur.fetchall()[-1]
        self.lineEdit.setText(information[1])  # получение названия и ввода его в строку
        self.textEdit.setText(information[3])  # получение описания и ввода его в строку
        self.btncolor1.setStyleSheet(
            "background-color: {}".format(colors[0]))  # получение цвета и его установление на задний фон
        if len(colors) == 2:
            self.btncolor2.setStyleSheet(
                "background-color: {}".format(colors[1]))
        if len(colors) == 3:
            self.btncolor2.setStyleSheet(
                "background-color: {}".format(colors[1]))
            self.btncolor3.setStyleSheet(
                "background-color: {}".format(colors[2]))
        self.btnnext.clicked.connect(self.close_event)

    def information(self):
        nameBrand = self.lineEdit.text()
        aboutBrand = self.textEdit.toPlainText()
        sql = 'UPDATE inform SET nameBrand = :nameBrand, description = :aboutBrand, colors = :colors'
        # изменение информации в БД
        self.cur.execute(sql, {"nameBrand": nameBrand, "aboutBrand": aboutBrand, "colors": ", ".join(colors)})
        self.db.commit()
        self.cur.close()  # Закрываем объект-курсор
        self.db.close()

    def close_event(self):
        result = QtWidgets.QMessageBox.question(self, "Подтверждение редактирования",
                                                "Вы действительно хотите изменить информацию?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
        # диалоговое окно подтверждения информации
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

    def choose_color(self):
        for el in colors:
            if el == color_now1[0]:
                del colors[colors.index(el)]
        ColorPage()
        self.btncolor1.setStyleSheet(
            "background-color: {}".format(color_now))  # установление нового цвета

    def choose_color1(self):
        for el in colors:
            if el == color_now2[0]:
                colors.pop(colors.index(el))
        ColorPage()
        self.btncolor2.setStyleSheet(
            "background-color: {}".format(color_now))  # установление нового цвета

    def choose_color2(self):
        for el in colors:
            if el == color_now3[0]:
                del colors[colors.index(el)]
        ColorPage()
        self.btncolor3.setStyleSheet(
            "background-color: {}".format(color_now))  # установление нового цвета


class Example(QWidget):
    def __init__(self):
        super().__init__()
        global flag
        self.initUI()
        global text, colors
        if ChangeInformation():
            self.close()
        flag = False

    def initUI(self):
        self.setWindowIcon(QIcon("images/pic/logoicon.ico"))
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Логотип')
        self.text = text
        self.show()

    def paintEvent(self, event):
        qp = QPainter()  # создание "события" рисованиия
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        color = ImageColor.getcolor(choice(colors), "RGB")  # hex меняется в rgb 
        qp.setPen(QColor(*color))  # установление цвета
        qp.setFont(QFont(choice(fonts), 70))  # выбор шрифта и его величины 
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)  # отрисовка
        qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPage()
    app.setStyle('Fusion')
    ex.show()
    sys.exit(app.exec_())
