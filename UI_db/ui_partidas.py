from customtkinter import *
from PIL import Image
import pandas as pd
import pygame as pg

class Partidas3T(CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master) # damos una referencia de la 
                                        # ventana 'principal'(UiMenu) a la clase 
                                        # padre CTkTopLevel
        
        #print(CTkToplevel.__bases__) # Para ver ºe donde hereda CTkTopLevel

        self.title('P')
        self.geometry('1280x720+200+40')
        self.resizable(0,0)

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
        self.partida.place(relx=0.705, rely=0.4, anchor='center') 

    # BOTONES
        # Cargar
        cargar = CTkButton(self.fondo, 
                         hover_color='#caa481', fg_color='#a2857a', bg_color='#f3e6db',
                         corner_radius=5,
                         text='Cargar', text_color='#dec1a5', font=('TypoGraphica',14),
                         width=250, height=55, command=self.cargarID)
        cargar.place(relx=0.605, rely=0.78, anchor = 'center')
        # Borrar
        borrar = CTkButton(self.fondo, 
                         hover_color='#caa481', fg_color='#a2857a', bg_color='#f3e6db',
                         corner_radius=5,
                         text='Borrar', text_color='#dec1a5', font=('TypoGraphica',14),
                         width=250, height=55)
        borrar.place(relx=0.805, rely=0.78, anchor = 'center')

#############################   LADO IZQUIERDO  ############################# 
        
    # BOTONES
        # Buscar
        buscar = CTkButton(self, 
            hover_color='#123456', fg_color='#654321', bg_color='#ffffff',
            corner_radius=5,
            text='Buscar', text_color='#ffffff', font=('TypoGraphica',14),
            width=180, height=50)
        buscar.place(relx=0.156, rely=0.694, anchor = 'center')
        # Guardar
        guardar = CTkButton(self, 
            hover_color='#123456', fg_color='#654321', bg_color='#ffffff',
            corner_radius=5,
            text='Guardar', text_color='#ffffff', font=('TypoGraphica',14),
            width=180, height=50, command=self.guardarID)
        guardar.place(relx=0.33, rely=0.694, anchor = 'center')
        # Input
        self.input = CTkTextbox(self,width=400,height=50,
            border_width=0,    
            font=('TypoGraphica',20),   
            fg_color='#123456', bg_color='#123456',
            text_color='#000000')
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
        ID = self.cargar_inp.get('0.0', 'end')[:-1]

        # Leer el archivo CSV en un DataFrame de pandasr
        df = pd.read_csv('./Partidas/Partidas3T.csv', dtype=str)

        try:
            # Filtrar el DataFrame para obtener la matriz deseada
            df_matriz = df[ID]
        except KeyError as e:
            print(f'No se encontró {ID}. Excepción: {e}')
            self.matriz_cargada = None
        else:    
            # Convertir el DataFrame filtrado a una matriz de NumPy
            tablero_aplanado = df_matriz.values

            # Reconstruir la matriz de 6 dimensiones
            forma_original = (3, 3, 3, 3, 3, 3)  # Esta debería ser la forma original de tu matriz
            
            self.matriz_cargada = tablero_aplanado.reshape(forma_original)


    def guardarID(self):
        ID = self.cargar_inp.get('0.0', 'end')[:-1]
        tablero = self.master.master.main.pantalla_actual.t3_set.tablero

        # Tu diccionario
        data = {ID: tablero.flatten()}
        
        try:
            csv = open('./Partidas/Partidas3T.csv')

        except FileNotFoundError as e:
            df = pd.DataFrame(data)
            df.to_csv('./Partidas/Partidas3T.csv', index=True)
            print(f'Creando DataFrame: {e}')

        else:
            csv.close()
            # Si existe, lee el archivo
            df = pd.read_csv('./Partidas/Partidas3T.csv')
            df[ID] = tablero.flatten()
            
            pg.image.save(pg.display.get_surface(), f"./Partidas/{ID}.png")
            self.fondo.configure(image = f'./Partidas/{ID}.png')

        # Guarda el DataFrame en un archivo .csv
        df.to_csv('./Partidas/Partidas3T.csv', index=False)
    



