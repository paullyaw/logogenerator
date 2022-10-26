import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QWidget

colorChanged = pyqtSignal()


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('logo1.ui', self)
        self.btncolor.clicked.connect(self.choose_color)

    def choose_color(self):
        colors = []
        color_pallete = QColorDialog(self)
        if color_pallete.exec_():
            colors.append(color_pallete.currentColor().name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPage()
    ex.show()
    sys.exit(app.exec_())
