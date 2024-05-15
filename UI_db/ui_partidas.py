from customtkinter import *
from PIL import Image
import os
import pandas as pd
import pygame as pg


class Partidas3T(CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master) # damos una referencia de la 
                                        # ventana 'principal'(UiMenu) a la clase 
                                        # padre CTkTopLevel
        
        self.title('Cagar - Guardar Partidas')
        self.geometry('1280x720+200+40')
        self.resizable(0,0)

        # https://stackoverflow.com/questions/75825190/how-to-put-iconbitmap-on-a-customtkinter-toplevel
        # En un foro de stackoverflow se menciona que trabajar con iconbitmap cuando se hereda de TopLevel
        # ocasiona problemas debido a que customtkinter cambia la foto del icono a las 250 milésimas de heredar.
        self.after(250, lambda: self.iconbitmap(('./Imagenes/UI/TTT.ico')))

        self.matriz_cargada = None

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
            width=178, height=50)
        buscar.place(relx=0.157, rely=0.6935, anchor = 'center')
        # Guardar
        guardar = CTkButton(self, 
            hover_color='#957569', fg_color='#8a6a5e', bg_color='#f3e6db',
            border_width=2.5, border_color='#ccb3a8', corner_radius=0, 
            text='Guardar', text_color='#ffffff', font=('TypoGraphica',14),
            width=178, height=50, command=self.guardarID)
        guardar.place(relx=0.33, rely=0.694, anchor = 'center')
    
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

    def cargarID(self):
        ID = self.input.get('0.0', 'end')[:-1]

        try:
            # Leer el archivo CSV en un DataFrame de pandasr
            df = pd.read_csv('./Partidas/Partidas3T.csv', dtype=str)
        except FileNotFoundError as e:
            print(f'{e}: Archivo CSV borrado')
        else:
            try:
                # Filtrar el DataFrame para obtener la matriz deseada
                matriz_cargada = df[ID]
            except KeyError as e:
                print(f'{e}: No se encontró {ID}')
                self.matriz_cargada = None
                self.cambiarFoto(None)
            else:    
                # Convertir el DataFrame filtrado a una matriz de NumPy
                tablero_aplanado = matriz_cargada.values
                # Reconstruir la matriz de 6 dimensiones
                forma_original = (3, 3, 3, 3, 3, 3)  # Esta debería ser la forma original de tu matriz
                self.matriz_cargada = tablero_aplanado.reshape(forma_original)

                self.cambiarFoto(ID)


    def guardarID(self):

        ID = self.input.get('0.0', 'end')[:-1]
        tablero = self.master.master.main.pantalla_actual.t3_set.tablero
        data = {ID: tablero.flatten()}
        
        # Crear - Modificar .csv
        try:
            csv = open('./Partidas/Partidas3T.csv')

        except FileNotFoundError as e:
            df = pd.DataFrame(data)
            df.to_csv('./Partidas/Partidas3T.csv', index=True) # index True es necesario?
            print(f'{e}: Creando DataFrame')

        else:
            csv.close()
            print('Modificando CSV existente.')
            df = pd.read_csv('./Partidas/Partidas3T.csv')
            df[ID] = tablero.flatten()
            
            # Guardar Imagen
            try:
                os.rename('./Partidas/EnEspera.png', f'./Partidas/{ID}.png')
            except FileNotFoundError as e:
                print(f'{e}: Foto de Partida "EnEspera" eliminada')
            else:
                foto_guardada = CTkImage(Image.open(f'./Partidas/{ID}.png'), size=(500,281))
                self.partida.configure(image = foto_guardada)
        finally:
            # Guarda el DataFrame en un archivo .csv
            df.to_csv('./Partidas/Partidas3T.csv', index=False)

    def cambiarFoto(self, ID):
        try:
            foto_cargada = CTkImage(Image.open(f'./Partidas/{ID}.png'), size=(500,281))
        except FileNotFoundError as e:
            print(f'{e}: Foto Partida Cargada')
        else:
            self.partida.configure(image=foto_cargada)
    



