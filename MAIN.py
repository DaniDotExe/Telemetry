import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QImage, QPixmap, QIcon

from oscuro import *

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form() 
        self.ui.setupUi(self)
        self.setWindowTitle("Laika")
        self.setWindowIcon(QIcon("./sources/layca_image.jpg"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


