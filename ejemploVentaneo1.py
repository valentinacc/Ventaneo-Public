from PySide6.QtWidgets import (
    QApplication,QPushButton,QCheckBox,QMainWindow, QLabel, QGridLayout, QWidget,QMessageBox, QStatusBar, QToolBar,QComboBox,QVBoxLayout,QDialog,QDialogButtonBox)
import sys


import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from pyqtgraph.Qt import QtGui, QtCore
from scipy.io import loadmat
from scipy import signal
from sklearn.linear_model import LinearRegression

from tkinter import filedialog
from os import path
from pathlib import Path
import scipy.io as sio

from PySide6.QtGui import QAction, QIcon
from pyqtgraph.Qt import QtGui, QtCore

def absPath(file):
    return str(Path(__file__).parent.absolute() / file)



class VentaneoClas(pg.GraphicsLayoutWidget):

    def __init__(self, parent,*args, **kwargs): 
        self.parent=parent       
        super().__init__(*args, **kwargs)

        self.arreglo1=[] #arreglo que guarda self.SENHAL que es la señal que viene de MainWindow
        y=[]
        vector=[]

        self.arreglo1=self.parent.ecg_Posiciones       

        if self.parent.canal1 != 0:     #canal1 es un bool definido en MainWindow

            print("arreglo1 en ventaneoR",self.arreglo1)               

            pos1=self.arreglo1[self.parent.posicionRventaneo] #ventaneoR(pos1) es un metodo que

            y,vector= self.parent.ventaneoR(pos1)              #tambien esta definido en Main     

            curva3 = self.p3.plot(pen='r')   
            curva3.setData(y,vector)

            self.parent.win3.show()
            
            #posicionRventaneo es una variable que se inicializa en el main y
            #deberia incrementarse cuando presiono cualquier tecla

            self.parent.posicionRventaneo += 1

          
# --------------------------------------------------------

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.construir_menu()
        self.construir_herramientas()
     

        self.win = pg.GraphicsLayoutWidget()
        self.win.resize(1000, 600)
        self.win.show() 

        self.posicionRventaneo=2
        
        self.canal1=0

        self.ecg_Posiciones=[40,50,60,70,100]

        # ecg1 = QCheckBox("ECG1")
        #  #self.setCentralWidget(ecg1)

       
        btn = QPushButton('Preprocesar')
        btn.clicked.connect(self.fuction) 

        cuadricula = QGridLayout()

        cuadricula.addWidget(btn, 3, 0)
        cuadricula.addWidget(self.win, 0, 2, 3, 1)

        widget = QWidget()
        widget.setLayout(cuadricula)

        self.setCentralWidget(widget)

        widget.setWindowTitle("Visualizador")    


    #-------------- Barra de Menu --------------------

    def construir_menu(self):
        menu = self.menuBar()
        menu_archivo = menu.addMenu("&Menú")

    #---------- SubVentana------------------------

        submenu_archivo1 = menu_archivo.addMenu("&Opciones")

        accion_zoomIn= QAction("Subventana &",self)
        accion_zoomIn.triggered.connect(self.subVentana)
        submenu_archivo1.addAction(accion_zoomIn)


    #-------------------------------------------------------
        menu_archivo.addSeparator()
        menu_archivo.addAction(QIcon(absPath("exit.png")), "S&alir", self.close, "Ctrl+Q")       
        menu_ayuda = menu.addMenu("Ay&uda")
        accion_info = QAction("&Información", self)
        accion_info.setIcon(QIcon(absPath("info.png")))
        accion_info.setShortcut("Ctrl+I")
        accion_info.triggered.connect(self.mostrar_info)
        accion_info.setStatusTip("Muestra información irrelevante")
        menu_ayuda.addAction(accion_info)
        self.setStatusBar(QStatusBar(self))

        # accesores de clase
        self.accion_info = accion_info

    def construir_herramientas(self):
        # Creamos una barra de herramientas
        herramientas = QToolBar("Barra de herramientas principal")
        # Podemos agregar la acción salir implícitamente
        herramientas.addAction(
            QIcon(absPath("exit.png")), "S&alir", self.close)
        # O añadir una acción ya creada para reutilizar código
        herramientas.addAction(self.accion_info)
        # La añadimos a la ventana principal
        self.addToolBar(herramientas)

    def mostrar_info(self):
        dialogo = QMessageBox.information(
            self, "Diálogo informativo", "Esto es un texto informativo")


    
    def fuction(self):

        print("Function")

        # ----- Carga el archivo------- 


        filepath = f'C:\\Users\\CRG-PC\\Desktop\pyqtgraph\\04936m_1h.mat'
        self.ECG=sio.loadmat(filepath)

        self.ecg1 = ((self.ECG ['val'][0])-0)/200
        self.ecg = np.transpose(self.ecg1)       # Señal a graficar
       
        self.fs = 250
        self.ts = 1/self.fs 

        self.t = np.linspace(0,np.size(self.ecg1),np.size(self.ecg1))*self.ts

        self.p = self.win.addPlot(title="ECG 1")
        self.p.showGrid(x = True, y = True)
        curva = self.p.plot(pen='y',name='ECG1')
        self.p.setRange(yRange=[-80, 80])
        self.p.setRange(xRange=[0, 3600])
        curva.setData(self.t,self.ecg)  #grafica del canal 1 

        if self.ecg!=[]:
            self.canal1=1
            print(self.canal1)


    #------------- ventana ---------------------   

    def subVentana(self,):

        self.win3 = VentaneoClas(title="Ventaneo", parent=self)

    def ventaneoR(self,posR):                       

        posPeak=posR                             
        inicio = (posPeak-5)
        
        fin = posPeak+3

        distancia = fin - inicio 

        y=np.zeros(distancia)
        vector=np.zeros(distancia)       
                        
        for r in range(0,distancia):                     
            vector[r]=self.ecg1[inicio+r]
            y[r]=self.t[inicio+r] 

        return y,vector




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
    