""" ui_menu.py

Este fichero es el responsable de crear la interfaz de la ventana secundaria del menú de selección de juegos.

El fichero utiliza el módulo DataBase.py, situado dentro de la carpeta UI_db, el cual contiene el código encargado
de administrar la tabla de usuarios. Además utiliza el módulo UI_db.ui_reglas encargado de la descripción de reglas para cada juego.

Al utilizar la librería customtkinter, hacemos uso de ella para herdar la clase CTkTopLevel, 
encargada de generar nuestra ventana secundaria para mostrar el menú.

Para utilizar el código, es necesaria la instalación de las librerías pillow y customtkinter en nuestro entorno virtual.
También hacemos uso de la librería pickle integrada en python.
"""

# Módulos
from UI_db.ui_reglas import UiReglas
from UI_db.ui_partidas import Partidas3T
from UI_db.DataBase import db_principal as db

# Librerías
from customtkinter import *
from PIL import Image  # Image para abrir imagenes dentro del proyecto                            
import pickle


class UiMenu(CTkToplevel):
    """
    La Clase UiMenu hereda de CTkToplevel. 
    Esta clase es responsable de crear la interfaz de la ventana secundaria del menú de selección de juegos.

    parent : CTkToplevel
        Crea un objeto de ventana secundaria

    Métodos
    -------
    __init__(self, master)
        Inicializa la clase con el master especificado.
    finalizar_UI(self)
        Cierra la aplicación.
    cambiar_foto(self)
        Cambia la foto del perfil del usuario.
    actualizar_punt(self)
        Actualiza los puntos del usuario.
    descripcion_1T(self)
        Muestra las reglas del juego 1.
    descripcion_2T(self)
        Muestra las reglas del juego 2.
    t1(self)
        Inicia el juego 1.
    t2(self)
        Inicia el juego 2.
    t3(self)
        Inicia el juego 3.
    m35(self)
        Inicia el juego m35.
    iniciar_juego(self, juego_elegido:str)
        Inicia el juego elegido.
    generarEasterEgg(self)
        Inicia el juego easter egg.
    generarPickle(self)
        Genera un archivo .pickle para guardar puntuaciones
    """

    def __init__(self, master):
        """
        Inicializa la clase con el master de UiLogin.
        """
        super().__init__(master=master) # Hay que especificar la clase Padre en la clase Hijo
        
        # Ajustes CTk                         
        self.title('TTT')
        self.geometry('1280x720+200+40')
        self.resizable(0,0)

        # https://stackoverflow.com/questions/75825190/how-to-put-iconbitmap-on-a-customtkinter-toplevel
        # En un foro de stackoverflow se menciona que trabajar con iconbitmap cuando se hereda de TopLevel
        # ocasiona problemas debido a que customtkinter cambia la foto del icono a las 250 milésimas de heredar.
        try:
            Image.open('./Imagenes/UI/TTT.png') 
        except FileNotFoundError:
            pass
        else:
            self.after(250, lambda: self.iconbitmap(('./Imagenes/UI/TTT.ico')))


        ######################       WIDGETS        #####################

        ### --- Fondo del menú --- ###
        img_menu = CTkImage(Image.open('./Imagenes/UI/Menu/menu.png'), size=(1280,720)) # la abrimos con PIL dentro de un CTkImage 
        fondo = CTkLabel(master=self, image=img_menu, text='')  # mostramos la foto en una etiqueta
        fondo.place(relx=0, rely=0, anchor='nw')

        ### --- Foto de Usuario --- ###
        foto_usuario_db = db.returnActivo()[1] # devolvemos la foto guardada en la base de datos

        try:
            foto_usuario_pil = CTkImage(Image.open(foto_usuario_db), size=(200,200))

        # No se encuentra la imagen en la ruta especificada
        except FileNotFoundError:
            print('Excepción: Sin foto de perfil')
            foto_usuario_pil = CTkImage(Image.open('./Imagenes/UI/Menu/foto_default.jpeg'), size=(200,200)) # Cargamos la foto default

        self.foto_cuadro = CTkLabel(self, image=foto_usuario_pil, text='', bg_color='#fceee2')  # mostramos la foto en una etiqueta
        self.foto_cuadro.place(relx=0.88, rely=0.3, anchor='center')             # blit en la pantalla 

    
        boton_foto = CTkButton(self, width=160, height=30, 
                            fg_color='#ede1d5', hover_color= '#c8beb4', bg_color = '#fceee2',
                            text='Cambiar foto', font=('TypoGraphica', 17), text_color='#a2857a', 
                            command=self.cambiar_foto)
        boton_foto.place(relx=0.88, rely=0.48,anchor='center')


        ### --- Estadísticas --- ###
        cuadro = CTkButton(self, border_width=2, text='', width=200, height=300,
                           border_color='#ede1d5', fg_color= '#fceee2', bg_color='#fceee2' , hover_color='#fceee2')
        cuadro.place(relx=0.88, rely=0.74,anchor='center')

        estadisticas_txt = CTkLabel(self, text='Estadisticas', font=('TypoGraphica', 18), text_color='#a2857a', bg_color='#fceee2')
        estadisticas_txt.place(relx=0.88, rely=0.56,anchor='center')


        # T1
        T1_txt = CTkLabel(self, text='T1', font=('TypoGraphica', 18), text_color='#a2857a', bg_color='#fceee2')
        T1_txt.place(relx=0.88, rely=0.62,anchor='center')

        self.T1_punt = CTkLabel(self, bg_color='#fceee2',
                                text = str(db.returnActivo()[2]), text_color='#a2857a', font=('TypoGraphica', 18))
                                
        self.T1_punt.place(relx=0.88, rely=0.65,anchor='center')

        # T2
        T2_txt = CTkLabel(self, text='T2', font=('TypoGraphica', 18), text_color='#a2857a', bg_color='#fceee2')
        T2_txt.place(relx=0.88, rely=0.7,anchor='center')

        self.T2_punt = CTkLabel(self, bg_color='#fceee2',
                                text = str(db.returnActivo()[3]), text_color='#a2857a', font=('TypoGraphica', 18))
                                
        self.T2_punt.place(relx=0.88, rely=0.73,anchor='center')


        
        ### --- Botón actualizar puntos --- ### 
        actualizar_img = CTkImage(Image.open('./Imagenes/UI/Menu/actualizar.png'), size=(27,27)) # la abrimos con PIL dentro de un CTkImage 
        b_act = CTkButton(self, 
                         fg_color='#ede1d5', hover_color= '#c8beb4', bg_color = '#fceee2',
                         corner_radius=10,
                         text='', image=actualizar_img,
                         width=80, height=20, command=self.actualizar_punt)
        b_act.place(relx=0.885,rely=0.9, anchor='center')


 
        ### --- Botones Descripción --- ###          
        b1_d = CTkButton(fondo, 
                         hover_color='#976042', fg_color='#b97a57', bg_color='#e0c2b6', #ccb3a8
                         corner_radius=0,
                         text='Descripcion     y      Reglas', text_color='#ffffff', font=('TypoGraphica', 17),
                         width=619.1, height=43.78, command=self.descripcion_1T)
        
        b1_d.place(relx=0.2492,rely=0.1307, anchor='nw')
        b2_d = CTkButton(fondo, 
                         hover_color='#976042', fg_color='#b97a57', bg_color='#e0c2b6',
                         corner_radius=0,
                         text='Descripcion     y      Reglas', text_color='#ffffff', font=('TypoGraphica', 17),
                         width=619.1, height=43.78, command=self.descripcion_2T)
        b2_d.place(relx=0.2492,rely=0.3493, anchor='nw') 
        b3_d = CTkButton(fondo, 
                         hover_color='#976042', fg_color='#b97a57', bg_color='#e0c2b6',
                         corner_radius=0,
                         text='Descripcion     y      Reglas', text_color='#ffffff', font=('TypoGraphica', 17),
                         width=619.1, height=43.78)
        b3_d.place(relx=0.2492,rely=0.577, anchor='nw')
        bm35_d = CTkButton(fondo, 
                         hover_color='#976042', fg_color='#b97a57', bg_color='#e0c2b6',font=('TypoGraphica', 17),
                         corner_radius=0,
                         text='Informacion', text_color='#ffffff', #a2857a
                         width=619.1, height=43.78, command=self.descripcion_M35)
        bm35_d.place(relx=0.2492,rely=0.8036, anchor='nw')

        ### --- Botones Jugar --- ### 
        b1_p = CTkButton(fondo, 
                         hover_color='#5a3c2b', fg_color='#704A35', bg_color='#e0c2b6',font=('TypoGraphica', 17),
                         corner_radius=0,
                         text='Jugar', text_color='#ffffff', 
                         width=619.1, height=63.8, command=self.t1)
        b1_p.place(relx=0.2492,rely=0.213, anchor='nw')
        b2_p = CTkButton(fondo, 
                         hover_color='#5a3c2b', fg_color='#704A35', bg_color='#e0c2b6',font=('TypoGraphica', 17),
                         corner_radius=0,
                         text='Jugar', text_color='#ffffff', 
                         width=619.1, height=63.8, command=self.t2)
        b2_p.place(relx=0.2492,rely=0.4316, anchor='nw')
        b3_p = CTkButton(fondo, 
                         hover_color='#5a3c2b', fg_color='#704A35', bg_color='#e0c2b6',font=('TypoGraphica', 17),
                         corner_radius=0,
                         text='Jugar', text_color='#ffffff', 
                         width=619.1, height=63.8, command=self.t3)
        b3_p.place(relx=0.2492,rely=0.659, anchor='nw')
        b4_p = CTkButton(fondo, 
                         hover_color='#5a3c2b', fg_color='#704A35', bg_color='#e0c2b6',font=('TypoGraphica', 17),
                         corner_radius=0,
                         text='Jugar', text_color='#ffffff', 
                         width=619.1, height=63.8, command=self.m35)
        b4_p.place(relx=0.2492,rely=0.885, anchor='nw')


        # Botón easter_egg
        b_eg = CTkButton(self, 
                         hover_color= '#b66e3f',fg_color='#b66e34', bg_color='transparent',font=('TypoGraphica', 17),
                         corner_radius=0,
                         text='',
                         width=18, height=18,
                         command=self.generarEasterEgg)
        b_eg.place(relx=0.116,rely=0.162, anchor='nw')
        self.contador = 0

        # EQUIVALENTE A → event.type == pg.QUIT 
        self.protocol("WM_DELETE_WINDOW", self.finalizar_UI)

    ######################       MÉTODOS DE ACTUALIZACIÓN        #####################   
    def finalizar_UI(self):
        """
        Finaliza el programa.
        """
        sys.exit()


    def cambiar_foto(self):
        """
        Cambia la foto del perfil del usuario. Se ejecuta al hacer click en el botón → cambiar foto.
        """

        foto_nueva = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")])
        usuario_activo = db.returnActivo()[0] # devolvemos el nombre
   
        # Puede ocurrir un error si al ejecutar filedialog.askopenfilename
        # no se selecciona ninguna foto. En vez de dejar la foto del usuario en la DB vacía
        # mantenemos la foto anterior para que no de problemas más adelante
        try:
            foto_usuario_pil = CTkImage(Image.open(foto_nueva), size=(200,200)) # la abrimos con PIL dentro de un CTKImage
                                                                                # puede dar error si no tenemos una ruta.
                                                                                # Ocurre si el usuario cierra filedialog  
                                                                                # sin cargar ninguna imagen.
        except:
            print('Excepción: No se seleccionó ninguna foto')
        
        else:
            db.modificarAtributo(usuario_activo, {'FOTO':foto_nueva})   # si no da fallos, la foto se actualiza en la db
            self.foto_cuadro.configure(image = foto_usuario_pil)        # hacemos el update de la foto aquí 
    
    def actualizar_punt(self):
        """
        Actualiza los puntos del usuario.
        """
        self.T1_punt.configure(text = str(db.returnActivo()[2]))
        self.T2_punt.configure(text = str(db.returnActivo()[3]))
        print(db) # Mostramos los datos usando la sobrecarga del operador


    def descripcion_1T(self):
        """
        Muestra las reglas del juego 1T.
        """
        self.withdraw() # ocultamos la pantalla menú
        imagen = Image.open('./Imagenes/UI/Reglas/T1_r.png')
        UiReglas(self, 'Reglas T1', imagen=imagen, hover_color='#3f4998',fg_color='#5763c5',x=0.1,y=0.8) 

    def descripcion_2T(self):
        """
        Muestra las reglas del juego 2T.
        """
        imagen = Image.open('./Imagenes/UI/Reglas/T2_r.png')
        self.withdraw() # ocultamos la pantalla menú
        UiReglas(self, 'Reglas 2T', imagen=imagen, hover_color='#976042',fg_color='#b97a57',x=0.1,y=0.9)
        
    def descripcion_3T(self):
        """
        Muestra las reglas del juego 3T.
        """
        imagen = Image.open('./Imagenes/UI/Reglas/T2_r.png')
        self.withdraw() # ocultamos la pantalla menú
        UiReglas(self, 'Reglas 2T', imagen=imagen, hover_color='#976042',fg_color='#b97a57',x=0.1,y=0.9)

    def descripcion_M35(self):
        """
        Muestra las reglas del juego M35.
        """
        imagen = Image.open('./Imagenes/UI/Reglas/M35_r.png')
        self.withdraw() # ocultamos la pantalla menú
        UiReglas(self, 'Reglas M35', imagen=imagen, hover_color='#f04e4e',fg_color='#e04948',x=0.1,y=0.85)

    def t1(self):
        """
        Inicia el juego 1T.
        """
        self.juego_elegido = '1t'
        self.iniciar_juego(self.juego_elegido)
    def t2(self):
        """
        Inicia el juego 2T.
        """
        self.juego_elegido = '2t'
        self.iniciar_juego(self.juego_elegido)
    def t3(self):
        """
        Inicia el juego 3T.
        """
        self.juego_elegido = '3t'
        self.iniciar_juego(self.juego_elegido)
    def m35(self):
        """
        Inicia el juego M35.
        """
        self.juego_elegido = 'm35'
        self.iniciar_juego(self.juego_elegido)
        

    def iniciar_juego(self, juego_elegido:str):
        """
        Inicia el juego elegido.

        Parámetros
        ----------
        juego_elegido : str
            El nombre del juego a iniciar.
        """

        self.withdraw() # ocultamos el menú
        self.quit()     # paramos temporalmente el mainloop(). 
                        # A partir de la segunda iteración en Pantalla se activa → elif == 'menu'

        try:
            self.master.main.pantalla_actual.cambio_pantalla = juego_elegido 
        # 'Game' object has no attribute 'pantalla_actual' (No se instanció Pantalla)
        except AttributeError: 
            self.master.main.juego_inicial = juego_elegido  # Sólo sirve en la primera iteración / primer juego
                                                            # Pantalla no se encuentra instanciada en la primera iteración


    def generarPickle(self):    
        """
        Genera un archivo.pickle para guardar puntuaciones. 
        Se usan excepciones para verificar la existencia del archivo antes de tratarlo
        """
        try:
            pickle_reader = open('easter_egg_score.pkl', 'rb')
        except FileNotFoundError:
            with open('easter_egg_score.pkl','wb') as pickle_writer:  
                pickle.dump(                                          
                    {'PERSONAL_HIGH_SCORES': {db.returnActivo()[0]: 0}, 
                     'GLOBAL_HIGH_SCORE': 0}, 
                    pickle_writer)
        else:
            scores = pickle.load(pickle_reader)
            if db.returnActivo()[0] not in scores['PERSONAL_HIGH_SCORES'].keys():  # Si existe, comprueba si hay
                scores['PERSONAL_HIGH_SCORES'][db.returnActivo()[0]] = 0           # datos del usuario actual
            pickle_reader.close()
            pickle_writer = open('easter_egg_score.pkl', 'wb')  # Actualizamos los datos
            pickle.dump(scores, pickle_writer)
            pickle_writer.close()

    def generarEasterEgg(self):
        """
        Genera la carga del juego easter egg.
        """
        self.contador += 1
        if self.contador == 3:
            self.contador = 0
            self.generarPickle()
            self.iniciar_juego('easter_egg')
    
    def instanciarPartidas3T(self):
        """
        Instancia la UI(CTkTopLevel) que permite guardar/cargar partidas.
        El método es llamado en Pantallla (bucle) → self.cambio_pantalla == 'guardar-cargar'
        """
        
        Partidas3T(master=self)