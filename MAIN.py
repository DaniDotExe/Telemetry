import collections
import math
import os
import sys
import threading
import time
from tracemalloc import start

import cv2
import geopandas as gpd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QRunnable, QSize, Qt, QThreadPool, pyqtSignal
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from serial import Serial

from oscuro_grafica import *

serialPort='COM11'
baudRate=9600
Samples = 20 
dataa=collections.deque([0]*Samples, maxlen=Samples)
dataa1=collections.deque([0]*Samples, maxlen=Samples)
dataa2=collections.deque([0]*Samples, maxlen=Samples)
valores=[0,0,0,0,0,0,0,0,0,0,0]
buffer=[0,0,0,0,0,0,0,0,0,0,0]
coor=[0,0]
acel=[0,0,0]
grav=[0,0,0]

#Clase para recibir los datos del equipo de comunicaciónes
class Worker(QtCore.QObject):

    finished = pyqtSignal()
    datos_sensor = pyqtSignal(int)
    datos_preasure=pyqtSignal(int)
    datos_altura=pyqtSignal(int)
    camera = pyqtSignal(np.ndarray)
    global dataa
    global dataa1
    global dataa2
    global coor
    global acel
    global grav
    global valores
    global buffer
    

    def getSerialData(self):
        
        os.chdir(r'C:\\Users\\juans\\OneDrive - UNIVERSIDAD INDUSTRIAL DE SANTANDER\\Instrumentacion\\Proyecto\\laika-main\\Camara')
        
        try:
            cap = cv2.VideoCapture(1)
        except:
            pass
        #objeto salida, contiene los parámetros para crear el video
        sal = cv2.VideoWriter('CanSat.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (640,480))
        valores=[0,0,0,0,0,0,0,0,0,0,0]
        buffer=[0,0,0,0,0,0,0,0,0,0,0]
        
        print('camera')
        if not cap.isOpened():
            print("Cannot open camera")
        Siempre = True
        i = 0
        while Siempre:
        #for j in range (100):
            i = i+1
            #time.sleep(.5)
            ret, frame = cap.read()
            name = 'Foto_' + str(i) + '.jpg'
            try:
                self.camera.emit(frame)
                sal.write(frame)
                cv2.imwrite(name, frame)
            except:
                pass

            self.datos_sensor.emit(i)
            print(i)
            try:
                serialConnection = Serial(serialPort, baudRate)
                print('--------------')                
                coor=[0,0]
                acel=[0,0,0]
                grav=[0,0,0]
                text=serialConnection.readline().strip()
                print(text)
                text=text.decode("utf-8",'ignore')
                print(text)
                #value=value.split('&')    
                kk=0
                                                   
                if text[0]=='*' and text[-1]=='*' and len(text)<30:
                    print("Trama 1")   
                    valor=text
                    valor=valor.replace('*','')
                    valor=valor.split('&')   
                    for j in range(5):
                        valores[j]=float(valor[j])
                        buffer[j]=float(valor[j])
                        
                    for j in range(5,len(valores)):
                        valores[j]=float(buffer[j])
                        
                elif text[0]=='#' and text[-1]=='#' and len(text)<30:
                    print("Trama 2")
                    valor=text
                    valor=valor.replace('#','')
                    valor=valor.split('&')
                    for j in range(5):
                        valores[j]=float(buffer[j])
                        
                    for j in range(5,len(valores)):
                        valores[j]=float(valor[kk])
                        kk=kk+1    

                elif text[0]=='*' and text[-1]=='#' and text[1]!='#':
                    print("Trama completa")
                    valor=text
                    valor=valor.replace('*#','&')
                    print(valor)
                    valor=valor.replace('*','')
                    valor=valor.replace('#','')
                    valor=valor.split('&')
             
                    for j in range(len(valor)):   
                        valores[j]=float(valor[j])
                        buffer[j]=float(valor[j])

                elif text[0]!='*' or text[0]!='#':
                    print("NN")
                    valores=buffer

                else:
                    print("Aqui")
                    valores=buffer
                
                print(buffer)
                print(valores)   
                
                dataa.append(valores[0])   #altura  %temperatura
                #lines.set_data(range(Samples),data)
                
                dataa1.append(valores[1])  #temperatura  %presion
                #lines1.set_data(range(Samples),data1)
                
                dataa2.append(valores[2])  #presion    %Altitud
                #lines2.set_data(range(Samples),data2)
                
                coor[0]=valores[3]  #lat
                coor[1]=valores[4]  #lon

                
                acel[0]=valores[5]  #aceleracion x
                acel[1]=valores[6]  #aceleracion y
                acel[2]=valores[7]  #aceleracion z    
                
                grav[0]=valores[8]  #gravitacional x
                grav[1]=valores[9]  #gravitacional y
                grav[2]=valores[10] #gravitacional z 
                    
                serialConnection.close()
            except:
                print("No se realizó conex")
                serialConnection = Serial(serialPort, baudRate)
                self.finished.emit()

#Ckase para generar la interfaz
class MainWindow(QMainWindow):

    global dataa1
    global dataa2
    global dataa
    global coor
    global acel
    global grav
    global valores
    global buffer
    lat = 0
    long = 0
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form() 
        self.ui.setupUi(self)
        self.setWindowTitle("Laika")
        self.setWindowIcon(QIcon("./sources/layca_image.jpg"))

        self.viewTemperature(1)
        self.viewPreasure()
        #self.viewAltura()
        self.on()
        self.viewMap()
    
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

        #viewPreasure
        #self.worker.dataa.connect(self.viewTemperature)
        self.worker.camera.connect(self.viewCam)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()

    def viewTemperature(self,datos_sensor):
        try:
            #print('Temperatura')
            self.lat = coor[0]
            self.long = coor[1]
            self.reloadMap()
            self.viewPreasure()
            self.viewAltura()
            datos = dataa
            datos= np.asarray(datos, dtype=None)
            #print(type(datos))
            #print("sensorr",dataa)
            index_datos = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)

            df=pd.DataFrame(datos, index_datos) 
            ax = df.plot()
            fig = ax.get_figure()
            plt.tick_params(axis='x', labelsize=18)
            plt.tick_params(axis='y', labelsize=18)
            plt.legend(loc="lower right",bbox_to_anchor=(9,9),labels= 'T')
            

            # set various colors
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white') 
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(colors='white', which='both')  # 'both' refers to minor and major axes

            fig = ax.get_figure()
                
            fig.savefig('temperature.png',transparent=True)
            plt.close(fig)
        
            pixmap = QPixmap('temperature.png')
            #Actualizamos la imagen
            self.ui.LIVE_14.setPixmap(pixmap)
            #self.ui.Titlle_124.setText(f'Altitud: {datos_sensor/2} [m]')
            self.ui.Titlle_125.setText(f'Temperatura: {datos[-1]} [°C]')
            self.ui.Titlle_129.setText(f'GPS [{self.lat}, {self.long}]')
            self.ui.Titlle_127.setText(f'Aceleración: [{acel[0],acel[1],acel[2]}] [m²/s]')
            self.ui.Titlle_128.setText(f'Orientación: [{grav[0],grav[1],grav[2]}]')
        except:
            pass

    def viewPreasure(self):
        try:
            #print('Presion')
            #self.lat = coor[0]
            #self.long = coor[1]
            #self.reloadMap()
            datos = dataa1
            datos= np.asarray(datos, dtype=None)
            #print(type(datos)) 
            #print(f'----------------Presion-------------{dataa2}')
            index_datos = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)


            df=pd.DataFrame(datos, index_datos) 
            ax = df.plot()
            fig = ax.get_figure()
            plt.tick_params(axis='x', labelsize=18)
            plt.tick_params(axis='y', labelsize=18)
            plt.legend(loc="lower right",bbox_to_anchor=(9,9),labels= 'T')

            # set various colors
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white') 
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(colors='white', which='both')  # 'both' refers to minor and major axes

            fig = ax.get_figure()
                
            fig.savefig('presion_image.png',transparent=True)
            plt.close(fig)
        
            pixmap = QPixmap('presion_image.png')
            #Actualizamos la imagen
            self.ui.LIVE_18.setPixmap(pixmap)
            #self.ui.Titlle_124.setText(f'Altitud: {datos_preasure/2} [m]')
            #self.ui.Titlle_125.setText(f'Temperatura: {datos[-1]} [°C]')
            self.ui.Titlle_126.setText(f'Presion: {datos[-1]} [Kpa]')
        except:
            pass 

    def viewAltura(self):
        try:
            #print('Altura')
            #self.lat = coor[0]
            #self.long = coor[1]
            #self.reloadMap()
            datos1 = dataa2
            datos1= np.asarray(datos1, dtype=None)
            #print(type(datos1))
            #print("sensorrP",datos1)
            index_datos = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)

            df=pd.DataFrame(datos1, index_datos) 
            ax = df.plot()
            fig = ax.get_figure()
            plt.tick_params(axis='x', labelsize=18)
            plt.tick_params(axis='y', labelsize=18)
            plt.legend(loc="lower right",bbox_to_anchor=(9,9),labels= 'T')

            # set various colors
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white') 
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(colors='white', which='both')  # 'both' refers to minor and major axes

            fig = ax.get_figure()
                
            fig.savefig('altura_imagen.png',transparent=True)
            plt.close(fig)
        
            pixmap = QPixmap('altura_imagen.png')
            #Actualizamos la imagen
            self.ui.LIVE_26.setPixmap(pixmap)
            self.ui.Titlle_124.setText(f'Altitud: {datos1[-1]} [m]')
        except:
            pass 

    def viewMap(self):
        print('Mapa')
        try:
            #path = 'C:\\Users\\juans\\OneDrive - UNIVERSIDAD INDUSTRIAL DE SANTANDER\\Instrumentacion\\Proyecto\\MGN2020_URB_MANZANA\\MGN_URB_MANZANA.shp'
            path = 'C:\\Users\\juans\\OneDrive - UNIVERSIDAD INDUSTRIAL DE SANTANDER\\Instrumentacion\\Proyecto\\MGN2020_URB_AREA_CENSAL\\MGN_URB_AREA_CENSAL.shp'

            Depto = gpd.read_file(path)
            Depto.head()

            self.Bmga = Depto[Depto['COD_MPIO'] == '68001'];
        except:
            pass

    def reloadMap(self):
        try:
            # self.lat = -73.117162
            # self.long = 7.140389

            textLabel="CanSat\n "+str(self.lat)+" \n"+str(self.long)

            # Control of the size of the map figure
            fig,ax = plt.subplots(figsize=(6, 9))
            plt.text(self.lat+(self.lat*0.00015),self.long-(self.long*0.001),textLabel, color = 'black')
            self.Bmga.plot(ax=ax);
            plt.scatter(self.lat,self.long, edgecolors ='black', color='red')

            # Control of title and axes
            ax.set_ylim([7.07,7.17])

            ax = plt.gca()
            plt.axis('off')

            fig = ax.get_figure()

            fig.savefig('imagen_map.png',transparent=True)
            plt.close(fig)

            pixmap = QPixmap('imagen_map.png')

            self.ui.LIVE_22.setPixmap(pixmap)

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
        