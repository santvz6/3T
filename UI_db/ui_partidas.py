""" ui_partidas.py

Este fichero es el responsable de crear la interfaz de la ventana terciaria del menú para guardar y cargar partidas.
Nuestra clase PartidasGuardadas hereda de CTkToplevel para así poder establecer una ventana terciaria.
CTkToplevel sigue usando el master de nuestra ventana principal para adquirir el mainloop() principal.

El fichero utiliza el módulo:
* cte: para utilizar datos constantes guardados

Para utilizar el código es necesaria la instalación de las siguientes librerías en nuestro entorno virtual:
* pillow: utilizado para el tratamiento de imagenes
* customtkinter: utilizado para la interfaz
* pandas: utilizado para guardar matrices, restricciones y turnos de cada partida en un archivo.csv
* numpy: utilizado para trabajar con las matrices del tablero

También utilizamos las librerías incorporadas en Python:
* sys: utilizado para salir del programa
* os: utilizado para renombrar y eliminar rutas de archivos
* shutil: utilizado para copiar achivos 
"""

# Librerías
from customtkinter import *
from PIL import Image
import pandas as pd
import numpy as np

import sys
import os
import shutil as sh

# Ficheros
import cte

class PartidasGuardadas(CTkToplevel):
    """
    La Clase PartidasGuardadas hereda de CTkToplevel. 
    Esta clase es responsable de crear la interfaz de la ventana terciaria del menú para guardar/cargar partidas.

    parent : CTkToplevel
        Crea un objeto de ventana terciaria

    Métodos
    -------
    __init__(self, master)
        Inicializa la clase con el master especificado.
    finalizar_UI(self)
        Finaliza el programa.
    volver_al_menu(self)
        Oculta la descripción y devuelve al usuario al menú
    buscarID(self)
        Busca el correspondiente ID en el .csv.
    guardarID(self)
        Guarda en el .csv el ID junto con la correspondiente matriz, restriccion y turno.
    cargarID(self)
        Carga en los atributos de t3_set los datos correspondientes. 
    borrarID(self)
        Borra la columna del .csv con el ID indicado
    cargarFoto(self)
        Cambia la foto del widget self.partida.
    """  
    
    def __init__(self, master):
        super().__init__(master=master) # damos una referencia de la 
                                        # ventana 'principal'(UiMenu) a la clase 
                                        # padre CTkTopLevel
        
        self.title('Cagar - Guardar Partidas')
        self.geometry('1280x720+200+40')
        self.resizable(0,0)

        self.after(250, lambda: self.iconbitmap(('./Imagenes/UI/TTT.ico')))

        self.matriz_cargada = ''
        self.restriccion_cargada = ''
        self.turno_cargado = ''
        self.ID_cargado = False
        self.ID_usada = ''

#############################   LADO DERECHO   ############################# 
    
    # IMAGENES
        # Fondo
        fondo_img = CTkImage(Image.open('./Imagenes/Partidas/Fondo3T.png'), size=(1280,720)) # la abrimos con PIL dentro de un CTkImage 
        self.fondo = CTkLabel(self, image=fondo_img, text='', bg_color='#fceee2')  # mostramos la foto en una etiqueta
        self.fondo.place(relx=0, rely=0, anchor='nw') 
        # Partida Seleccionada
        partida = CTkImage(Image.open('./Imagenes/Partidas/Default.png'), size=(500,281)) # la abrimos con PIL dentro de un CTkImage 
        self.partida = CTkLabel(self, image=partida, text='', bg_color='#fceee2')  # mostramos la foto en una etiqueta
        self.partida.place(relx=0.705, rely=0.40264, anchor='center') 

    # BOTONES
        # Cargar
        cargar = CTkButton(self.fondo, 
            hover_color='#957569', fg_color='#8a6a5e', bg_color='#f3e6db',
            border_width=2.5, border_color='#ccb3a8', corner_radius=0, 
            text='Cargar', text_color='#ffffff', font=('TypoGraphica',14),
            width=250, height=55, command=self.cargarID)
        cargar.place(relx=0.605, rely=0.78, anchor = 'center')
        # Borrar
        borrar = CTkButton(self.fondo, 
            hover_color='#957569', fg_color='#8a6a5e', bg_color='#f3e6db',
            border_width=2.5, border_color='#ccb3a8', corner_radius=0, 
            text='Borrar', text_color='#ffffff', font=('TypoGraphica',14),
            width=250, height=55, command=self.borrarID)
        borrar.place(relx=0.805, rely=0.78, anchor = 'center')

#############################   LADO IZQUIERDO  ############################# 
        
    # BOTONES
        # Buscar
        buscar = CTkButton(self, 
            hover_color='#957569', fg_color='#8a6a5e', bg_color='#f3e6db',
            border_width=2.5, border_color='#ccb3a8', corner_radius=0, 
            text='Buscar', text_color='#ffffff', font=('TypoGraphica',14),
            width=178, height=50, command=self.buscarID)
        buscar.place(relx=0.157, rely=0.694, anchor = 'center')
        # Guardar
        guardar = CTkButton(self, 
            hover_color='#957569', fg_color='#8a6a5e', bg_color='#f3e6db',
            border_width=2.5, border_color='#ccb3a8', corner_radius=0, 
            text='Guardar', text_color='#ffffff', font=('TypoGraphica',14),
            width=178, height=50, command=self.guardarID)
        guardar.place(relx=0.33, rely=0.694, anchor = 'center')
        # Salir
        guardar = CTkButton(self, 
            hover_color='#957569', fg_color='#8a6a5e', bg_color='#f3e6db',
            border_width=2.5, border_color='#ccb3a8', corner_radius=0, 
            text='Salir', text_color='#ffffff', font=('TypoGraphica',14),
            width=400, height=50, command=self.volver_al_menu)
        guardar.place(relx=0.2435, rely=0.825, anchor = 'center')
    
    # TEXTBOX    
        # Input
        self.input = CTkTextbox(self,width=400,height=50,
            fg_color='#a2857a', bg_color='#f3e6db',
            border_width=2.5, border_color='#ccb3a8', corner_radius=0, 
            font=('Bahnschrift Bold Semi-Condensed',20),   
            text_color='#ffffff')
        self.input.place(relx=0.245, rely=0.563, anchor = 'center')


    
        # EQUIVALENTE A → event.type == pg.QUIT 
        self.protocol("WM_DELETE_WINDOW", self.finalizar_UI)

    ######################       MÉTODOS DE ACTUALIZACIÓN        #####################   
    def finalizar_UI(self):
        """
        Finaliza el programa.
        """
        sys.exit()
        
    def volver_al_menu(self):
        """
        Oculta la descripción y devuelve al usuario al menú
        """
        self.master.deiconify() # Mostramos UiMenu
        self.withdraw()         # Ocultamos PartidasGuardadas

    def buscarID(self):
        """
        Busca el correspondiente ID en el .csv
        """
        ID = self.input.get('0.0', 'end')[:-1]

        
    #### EXISTENCIA ARCHIVO CSV ####
        try:
            df = pd.read_csv('./Partidas/Partidas3T.csv', dtype=str)

        # NO existe
        except FileNotFoundError as e:      
            print(f'{e}: Sin partidas guardadas. Guardando: {ID}')
            self.guardarID() # Guardamos la partida dado que no existe ninguna más
            self.ID_cargado = ID

        # SÍ existe
        else:     
        #### EXISTENCIA ID ####                      
            try:
                df[ID]   
            # ID NO existe
            except KeyError as e:   
                print(f'{e}: No se encontró {ID}')
                self.ID_cargado = False
                self.cargarFoto(None)

            # ID SÍ existe
            else:   
                # Carga de Datos
                self.ID_cargado = ID
                matriz = df[ID].iloc[:len(df[ID])-5]
                restriccion = df[ID].iloc[len(df[ID])-5:-1]
                
                # Conversión Tipo de Dato
                self.matriz_cargada = matriz.values.reshape((3, 3, 3, 3, 3, 3)) # .values: NumPy, list(): Pyhton Vanilla
                self.restriccion_cargada = tuple(restriccion.values.astype(int))
                self.turno_cargado = df[ID].iloc[-1]
                self.cargarFoto(ID)
                
    def guardarID(self):
        """
        Guarda en el .csv el ID junto con la correspondiente matriz, restriccion y turno
        """
        ID = self.input.get('0.0', 'end')[:-1]
        tablero = self.master.master.main.pantalla_actual.t3_set.tablero
        restriccion = np.array(self.master.master.main.pantalla_actual.t3_set.restriccion)
        turno = np.array([self.master.master.main.pantalla_actual.t3_set.actual.nombre])

        values = np.concatenate((tablero.flatten(), restriccion, turno))
        data = {ID: values}

        
    #### EXISTENCIA ARCHIVO CSV ####
        try:
            csv = open('./Partidas/Partidas3T.csv')            
        # CREAR + GUARDAR
        except FileNotFoundError as e:
            print(f'{e}: Creando DataFrame')
            df = pd.DataFrame(data)

            os.rename('./Partidas/EnEspera.png', f'./Partidas/{ID}.png')
            self.ID_usada = ID
            
            # Carga de Datos
            matriz = df[ID].iloc[:len(df[ID])-5]
            restriccion = df[ID].iloc[len(df[ID])-5:-1]
            
            # Conversión Tipo de Dato
            self.matriz_cargada = matriz.values.reshape((3, 3, 3, 3, 3, 3)) # .values: NumPy, list(): Pyhton Vanilla
            self.restriccion_cargada = tuple(restriccion.values.astype(int))
            self.turno_cargado = df[ID].iloc[-1]
            self.cargarFoto(ID=ID)
            
            df.to_csv('./Partidas/Partidas3T.csv', index=False)
            print(f'Guardado exitoso: {ID}')        
            
            
        # LEER
        else:
            csv.close()  
            df = pd.read_csv('./Partidas/Partidas3T.csv') # leemos CSV existente      
        
        #### EXISTENCIA ID EN CSV ####
            try:
                df[ID]
            # ID INEXISTENTE + ...
            except KeyError:
            #### ¿FOTO EnEspera? ####
                try:
                    os.rename('./Partidas/EnEspera.png', f'./Partidas/{ID}.png')
                # Foto USADA
                except FileNotFoundError:
                    sh.copy(f'./Partidas/{self.ID_usada}.png', f'./Partidas/{ID}.png')
                # Foto EnEspera   
                else:
                    # El primer guardado de Imagen no ocasiona problemas (Imagen=EnEspera.png). Pero si el usuario quiere guardar
                    # la misma partida ambas veces tendremos que reutilizar la misma foto (Imagen=ID.png). Es por esto que guardamos
                    # el ID, para localizar la imagen renombrada y copiarla usando shutil.copy().
                    self.ID_usada = ID  

                # ... + GUARDAR
                df[ID] = values
                
                # Carga de Datos
                matriz = df[ID].iloc[:len(df[ID])-5]
                restriccion = df[ID].iloc[len(df[ID])-5:-1]
                self.ID_cargado = ID
                
                # Conversión Tipo de Dato
                self.matriz_cargada = matriz.values.reshape((3, 3, 3, 3, 3, 3)) # .values: NumPy, list(): Pyhton Vanilla
                self.restriccion_cargada = tuple(restriccion.values.astype(int))             
                self.turno_cargado = df[ID].iloc[-1]
                self.cargarFoto(ID=ID)
                
                df.to_csv('./Partidas/Partidas3T.csv', index=False)
                print(f'Guardado exitoso: {ID}')

            # ID EXISTENTE 
            else:
                print(f'Partida: {ID} existente')
                
    def cargarID(self):
        """
        Carga en los atributos de t3_set los datos correspondientes
        """
        if self.ID_cargado:
            self.master.master.main.pantalla_actual.t3_set.tablero = self.matriz_cargada
            self.master.master.main.pantalla_actual.t3_set.restriccion = self.restriccion_cargada
            self.master.master.main.pantalla_actual.t3_set.cargar_turno(self.turno_cargado)
            self.master.deiconify()
            self.withdraw()         
        else:
            print('Selecciona Una Partida Guardada')

    def borrarID(self):
        """
        Borra la columna del .csv con el ID indicado
        """
        if self.ID_cargado:
            print('Intetnando borrar')
            df = pd.read_csv('./Partidas/Partidas3T.csv')
            df = df.drop(columns=[self.ID_cargado])
            df.to_csv('./Partidas/Partidas3T.csv', index=False)
            try:
                os.remove(f'./Partidas/{self.ID_cargado}.png')
            except FileNotFoundError as e:
                print(f'{e}: Foto Inexistente')

    def cargarFoto(self, ID):
        """
        Cambia la foto del widget self.partida.
        """
        try:
            foto_cargada = CTkImage(Image.open(f'./Partidas/{ID}.png'), size=(500,281))
        
        # Si la Foto del ID ha sido eliminada
        except FileNotFoundError as e:
            print(f'{e}: Foto Default Cargada')
            self.partida.configure(image=CTkImage(Image.open(cte.partida_default), size=(500,281)))

        else:
            self.partida.configure(image=foto_cargada)