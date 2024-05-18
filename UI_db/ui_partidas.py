""" ui_partidas.py

Este fichero es el responsable de crear la interfaz de la ventana secundaria 
encargada de la gestión de partidas. En ella podremos guardar, cargar, buscar y borrar partidas del juego 3T.

Para la creación de la interfaz se utiliza la librería customtkinter.
Además, para instanciar una venta secundaria, heredamos de la clase CTkTopLevel.

Este fichero se encarga de crear un archivo .csv y guardar en él la matriz, restricción y turno de una partida en un juego llamado 3T. 
Esto permite a los usuarios guardar y cargar partidas, mejorando la experiencia de juego.

Para utilizar el código, es necesaria la instalación de las librerías pillow y customtkinter en nuestro entorno virtual. 
También hacemos uso de las librerías pandas y numpy para el manejo de datos.
"""

# Librerías
from customtkinter import *
from PIL import Image
import pandas as pd
import numpy as np

import os
import shutil as sh

# Ficheros
import cte


class Partidas3T(CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master) # damos una referencia de la 
                                        # ventana 'principal'(UiMenu) a la clase 
                                        # padre CTkTopLevel
        
        self.title('Cagar - Guardar Partidas')
        self.geometry('1280x720+200+40')
        self.resizable(0,0)

        self.after(250, lambda: self.iconbitmap(('./Imagenes/UI/TTT.ico')))

        self.matriz_cargada = False
        self.restriccion_cargada = False
        self.turno_cargado =False
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
            width=250, height=55)
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
            width=400, height=50)
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
        self.master.deiconify() # mostramos master de nuevo (master representa el self de un nivel superior / UiMenu) 
        self.withdraw()         # ocultamos Descripción

    def buscarID(self):
        ID = self.input.get('0.0', 'end')[:-1]

        
        # El archivo .csv puede no exisitir
        try:
            df = pd.read_csv('./Partidas/Partidas3T.csv', dtype=str)

        # NO existe
        except FileNotFoundError as e:      
            print(f'{e}: Sin partidas guardadas. Guardando: {ID}')
            self.guardarID() # Guardamos la partida dado que no existe ninguna más

        # SÍ existe
        else:                       
            
            # La matriz[ID] puede no exisitir
            try:
                df[ID]
            
            # NO existe
            except KeyError as e:   
                print(f'{e}: No se encontró {ID}')
                self.turno_cargado = False

                self.cambiarFoto(None)
            # SÍ existe
            else:   
                # Carga de Datos
                matriz = df[ID].iloc[:len(df[ID])-5]
                restriccion = df[ID].iloc[len(df[ID])-5:-1]
                
                # Conversión Tipo de Dato
                self.matriz_cargada = matriz.values.reshape((3, 3, 3, 3, 3, 3)) # .values: NumPy, list(): Pyhton Vanilla
                self.restriccion_cargada = tuple(restriccion.values.astype(int))
                self.turno_cargado = df[ID].iloc[-1]
                self.cambiarFoto(ID)

    def guardarID(self):

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
            self.cambiarFoto(ID=ID)
            
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
                
                # Conversión Tipo de Dato
                self.matriz_cargada = matriz.values.reshape((3, 3, 3, 3, 3, 3)) # .values: NumPy, list(): Pyhton Vanilla
                self.restriccion_cargada = tuple(restriccion.values.astype(int))             
                self.turno_cargado = df[ID].iloc[-1]
                self.cambiarFoto(ID=ID)
                
                df.to_csv('./Partidas/Partidas3T.csv', index=False)
                print(f'Guardado exitoso: {ID}')

            # ID EXISTENTE 
            else:
                print(f'Partida: {ID} existente')
                
             
    
    def cargarID(self):
        if self.turno_cargado:
            self.master.master.main.pantalla_actual.t3_set.tablero = self.matriz_cargada
            self.master.master.main.pantalla_actual.t3_set.restriccion = self.restriccion_cargada
            self.master.master.main.pantalla_actual.t3_set.cargar_turno(self.turno_cargado)
            self.master.deiconify()
            self.withdraw()         
        else:
            print('Selecciona Una Partida Guardada')


    def cambiarFoto(self, ID):
        try:
            foto_cargada = CTkImage(Image.open(f'./Partidas/{ID}.png'), size=(500,281))
        
        # Si la Foto del ID ha sido eliminada
        except FileNotFoundError as e:
            print(f'{e}: Foto Default Cargada')
            self.partida.configure(image=CTkImage(Image.open(cte.partida_default), size=(500,281)))

        else:
            self.partida.configure(image=foto_cargada)

    def salir(self):
        self.master.deiconify()
        self.withdraw()
