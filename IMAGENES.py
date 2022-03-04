import sys
import pandas as pd
import matplotlib.pyplot as plt 

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5 import QtWidgets, QtCore

import time

from oscuro_grafica import *

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form() 
        self.ui.setupUi(self)
        self.setWindowTitle("Laika")
        self.setWindowIcon(QIcon("./sources/layca_image.jpg"))
        self.viewTemperature()

    def viewTemperature(self):
        datos = (0,1,2,3,4,3)
        index_datos = (0,1,2,3,4,5)

        df=pd.DataFrame(datos, index_datos) 
        ax = df.plot()
        fig = ax.get_figure()
        plt.tick_params(axis='x', labelsize=18)
        plt.tick_params(axis='y', labelsize=18)

        # set various colors
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(colors='white', which='both')  # 'both' refers to minor and major axes

        fig = ax.get_figure()
            
        fig.savefig('imagen.png',transparent=True)
        plt.close(fig)
    
        pixmap = QPixmap('imagen.png')
        #Actualizamos la imagen
        self.ui.LIVE_14.setPixmap(pixmap)     


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()



        