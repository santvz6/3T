""" ui_reglas.py

Este fichero es el responsable de crear la interfaz de la ventana terciaria del menú para leer las reglas.
Nuestra clase UiReglas hereda de CTkToplevel para así poder establecer una ventana terciaria.
CTkToplevel sigue usando el master de nuestra ventana principal para adquirir el mainloop() principal.

El fichero utiliza el módulo:
* cte: para utilizar datos constantes guardados

Para utilizar el código es necesaria la instalación de las siguientes librerías en nuestro entorno virtual:
* customtkinter: utilizado para la interfaz

También utilizamos las librerías incorporadas en Python:
* sys: utilizado para salir del programa 
"""

# Librerías
from customtkinter import *
import sys

class UiReglas(CTkToplevel):
    """
    La Clase UiReglas hereda de CTkToplevel. 
    Esta clase es responsable de crear la interfaz de la ventana terciaria del menú de reglas.

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
    """
    
    def __init__(self, master, title:str, imagen, 
                 hover_color:str, fg_color:str,
                 x:int, y:int):
        super().__init__(master=master) # damos una referencia de la 
                                        # ventana 'principal'(UiMenu) a la clase 
                                        # padre CTkTopLevel
        
        #print(CTkToplevel.__bases__) # Para ver ºe donde hereda CTkTopLevel

        self.title(title)
        self.geometry('1280x720+200+40')
        self.resizable(0,0)
        self.after(250, lambda: self.iconbitmap(('./Imagenes/UI/TTT.ico')))

        fondo_img = CTkImage(imagen, size=(1280,720)) 
        fondo = CTkLabel(self, image=fondo_img, text='', bg_color='#fceee2')  
        fondo.place(relx=0, rely=0, anchor='nw')       

        volver_menu = CTkButton(fondo, 
                         hover_color=hover_color, fg_color=fg_color, bg_color='#ffffff',
                         corner_radius=3,
                         text='Volver  al  menu', text_color='#ffffff', font=('TypoGraphica',14),
                         width=200, height=43.78, command=self.volver_al_menu)
        volver_menu.place(relx=x, rely=y, anchor = 'nw')
        
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
        self.master.deiconify() # mostramos UiMenu 
        self.withdraw()         # ocultamos UiReglas