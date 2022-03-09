import sys
from tracemalloc import start
import pandas as pd
import matplotlib.pyplot as plt 

from PyQt5.QtCore import QSize, Qt, pyqtSignal, QRunnable, QThreadPool
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5 import QtWidgets, QtCore
import threading
import time
import collections
from matplotlib.lines import Line2D
import matplotlib.animation as animation
import numpy as np 
import math
#from serial import Serial

import time
import cv2
from oscuro_grafica import *

serialPort='COM20'
baudRate=9600

class Worker(QtCore.QObject):

    finished = pyqtSignal()
    datos_sensor = pyqtSignal(int)
    camera = pyqtSignal(np.ndarray)

    def getSerialData(self):

        cap = cv2.VideoCapture(0)
        print('camera')
        if not cap.isOpened():
            print("Cannot open camera")
    
        Siempre = True
        i = 0
        while Siempre:
        #for j in range (100):
            i = i+1
            time.sleep(.5)
            ret, frame = cap.read()
            self.camera.emit(frame)
            self.datos_sensor.emit(i)
            print(i)

        self.finished.emit()

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form() 
        self.ui.setupUi(self)
        self.setWindowTitle("Laika")
        self.setWindowIcon(QIcon("./sources/layca_image.jpg"))

        self.viewTemperature(1)
        self.on()

        #self.timer = QtCore.QTimer()
        #self.timer.start(1000)
        #self.timer.timeout.connect(self.viewCam)
        #self.timer.timeout.connect(self.on)
        #self.timer.timeout.connect(self.viewTemperature)
    
    def on(self):
        # Step 2: Create a QThread object
        self.thread = QtCore.QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.getSerialData)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.datos_sensor.connect(self.viewTemperature)
        self.worker.camera.connect(self.viewCam)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()

    def viewTemperature(self,datos_sensor):
        try:
            print('Temperatura')
            datos = (datos_sensor-1,datos_sensor,datos_sensor,datos_sensor,datos_sensor,datos_sensor*2)
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
            self.ui.Titlle_124.setText(f'Altitud: {datos_sensor/2} [m]')
            self.ui.Titlle_125.setText(f'Temperatura: {datos_sensor} [°C]')
        except:
            pass 

    def viewCam(self,frame):
        print('Camara')
        try:
            #ret, frame = cap.read()
            image_detect = frame
            #conversion a RGB
            image = cv2.cvtColor(image_detect, cv2.COLOR_BGR2RGB)
            #obtener datos de imagen
            height, width, channel = image.shape
            step= channel*width
            #crear QImage para imagen
            qImg=QImage(image.data,width,height,step,QImage.Format_RGB888)
            #mostrar en el label
            self.ui.LIVE_19.setPixmap(QPixmap.fromImage(qImg))
        except:
            pass
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()



        