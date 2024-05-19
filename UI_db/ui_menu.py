""" ui_menu.py
Este fichero es el responsable de crear la interfaz de la ventana secundaria del menú de selección de juegos.
Nuestra clase UiMenu hereda de CTkTopleve para así poder establecer una ventana secundaria.
CTkToplevel sigue usando el master de nuestra ventana principal para adquirir el mainloop() principal.

El fichero utiliza los módulos:
* UI_db.DataBase:  contiene el código encargado de administrar la tabla de usuarios.
* UI_db.ui_reglas: la instanica de esta clase conlleva la creación de una venta terciaria que hereda de CTkToplevel
* UI_db.ui_partidas: la instanica de esta clase conlleva la creación de una venta terciaria que hereda de CTkToplevel

Para utilizar el código es necesaria la instalación de las siguientes librerías en nuestro entorno virtual:
* pillow: utilizado para el tratamiento de imagenes
* customtkinter: utilizado para la interfaz

También utilizamos las librerías incorporadas en Python:
* sys: utilizado para salir del programa
* pickle: utilizado para la creación de un archivo.pickle, en él se guarda la información del Easter Egg
"""

# Módulos
from UI_db.DataBase import db_principal as db
from UI_db.ui_reglas import UiReglas
from UI_db.ui_partidas import PartidasGuardadas

# Librerías
from customtkinter import *
from PIL import Image  # Image para abrir imagenes dentro del proyecto                            
import sys
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
        Finaliza el programa.
    cambiar_foto(self)
        Cambia la foto del perfil del usuario.
    actualizar_punt(self)
        Actualiza los puntos del usuario.
    instanciar_descripcion(funcion)
        Instancia la descripción elegida.
    descripcion_1T(self)
        Muestra las reglas del juego 1T.
    descripcion_2T(self)
        Muestra las reglas del juego 2T.
    descripcion_3T(self)
        Muestra las reglas del juego 3T.
    descripcion_M35(self)
        Muestra las reglas del juego M35.
    iniciar_juego(funcion)
        Inicia el juego elegido.
    iniciar1t(self)
        Inicia el juego 1T.
    iniciar2t(self)
        Inicia el juego 2T.
    iniciar3t(self)
        Inicia el juego 3T.
    iniciarm35(self)
        Inicia el juego M35.
    iniciarEasterEgg(self)
        Inicia el juego EasterEgg
    generarEasterEgg(self)
        Genera la inicialización del EasterEgg
    generarPickle(self)
        Genera un archivo.pickle para guardar puntuaciones.
    instanciarPartidas3T(self)
        Instancia la UI(CTkTopLevel) que permite guardar/cargar partidas.
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
        except FileNotFoundError as e:
            print(f'{e}: No se ha podido establecer el icono')
        else:
            self.after(250, lambda: self.iconbitmap(('./Imagenes/UI/TTT.ico')))


############################################       WIDGETS        ###########################################

### IMAGENES ############

    ### FONDO 
        menu_imagen = CTkImage(Image.open('./Imagenes/UI/Menu/menu.png'), size=(1280,720))  
        fondo = CTkLabel(master=self, image=menu_imagen, text='')  # mostramos la foto en una etiqueta
        fondo.place(relx=0, rely=0, anchor='nw')
    
    ### FOTO PERSONAL
        foto_usuario_db = db.returnActivo()[1]

        try:
            foto_usuario_pil = CTkImage(Image.open(foto_usuario_db), size=(200,200))
        except FileNotFoundError as e:
            # Cargamos la foto default            
            foto_usuario_pil = CTkImage(Image.open('./Imagenes/UI/Menu/foto_default.jpeg'), size=(200,200)) 
            print(f'{e}: Sin foto de perfil')
        
        self.foto_cuadro = CTkLabel(self, image=foto_usuario_pil, text='', bg_color='#fceee2')
        self.foto_cuadro.place(relx=0.88, rely=0.3, anchor='center')                 

### ETIQUETAS ###########
    ### PUNTUACIONES
        # Actúa como una superificie
        superficie_puntuacion = CTkButton(self, border_width=2, text='', width=200, height=300,
                           border_color='#ede1d5', fg_color= '#fceee2', bg_color='#fceee2' , hover_color='#fceee2')
        superficie_puntuacion.place(relx=0.88, rely=0.74,anchor='center')

        ### Texto Puntuación
        puntuaciones_texto = [
            {'text': 'Estadisticas', 'rely': 0.56},
            {'text': 'T1', 'rely': 0.62},
            {'text': 'T2', 'rely': 0.68},
            {'text': 'T3', 'rely': 0.74},
            {'text': 'M35', 'rely': 0.8},
        ]

        for puntuacion_texto in puntuaciones_texto:
            punt_str = CTkLabel(self, text=puntuacion_texto['text'], font=('TypoGraphica', 18), text_color='#a2857a', bg_color='#fceee2')
            punt_str.place(relx=0.88, rely=puntuacion_texto['rely'],anchor='center')

        ### Cantidad Puntuación
        self.T1_punt = CTkLabel(self, bg_color='#fceee2',
            text = str(db.returnActivo()[2]), text_color='#a2857a', font=('TypoGraphica', 18))                     
        self.T2_punt = CTkLabel(self, bg_color='#fceee2',
            text = str(db.returnActivo()[3]), text_color='#a2857a', font=('TypoGraphica', 18))              
        self.T3_punt = CTkLabel(self, bg_color='#fceee2',
            text = str(db.returnActivo()[4]), text_color='#a2857a', font=('TypoGraphica', 18))              
        self.M35_punt = CTkLabel(self, bg_color='#fceee2',
            text = str(db.returnActivo()[5]), text_color='#a2857a', font=('TypoGraphica', 18)) 
        
        self.T1_punt.place(relx=0.88, rely=0.65,anchor='center')
        self.T2_punt.place(relx=0.88, rely=0.71,anchor='center')   
        self.T3_punt.place(relx=0.88, rely=0.77,anchor='center')          
        self.M35_punt.place(relx=0.88, rely=0.83,anchor='center')


### BOTONES #############
    ### FOTO PERSONAL    
        boton_foto = CTkButton(self, width=160, height=30, 
                            fg_color='#ede1d5', hover_color= '#c8beb4', bg_color = '#fceee2',
                            text='Cambiar foto', font=('TypoGraphica', 17), text_color='#a2857a', 
                            command=self.cambiar_foto)
        boton_foto.place(relx=0.88, rely=0.48,anchor='center')


    ### PUNTUACIONES 
        refresh_img = CTkImage(Image.open('./Imagenes/UI/Menu/actualizar.png'), size=(27,27))
        b_actualizar = CTkButton(self, 
                         fg_color='#ede1d5', hover_color= '#c8beb4', bg_color = '#fceee2',
                         corner_radius=10,
                         text='', image=refresh_img,
                         width=80, height=20, command=self.actualizar_punt)
        b_actualizar.place(relx=0.885,rely=0.9, anchor='center')


    ### DESCRIPCIONES                 
        descripciones = [
            {'command': self.descripcion_1T, 'rely': 0.1307},
            {'command': self.descripcion_2T, 'rely': 0.3493},
            {'command': self.descripcion_3T, 'rely': 0.577},
            {'command': self.descripcion_M35, 'rely': 0.8036}
        ]

        for descripcion in descripciones:
            b_descripcion = CTkButton(fondo, 
                                    hover_color='#976042', fg_color='#b97a57', bg_color='#e0c2b6',
                                    corner_radius=0,
                                    text='Descripcion     y      Reglas', text_color='#ffffff', font=('TypoGraphica', 17),
                                    width=619.1, height=43.78, command=descripcion['command'])
            b_descripcion.place(relx=0.2492, rely=descripcion['rely'], anchor='nw')

        botones_jugar = [
            {'command': self.iniciar1t, 'rely': 0.213},
            {'command': self.iniciar2t, 'rely': 0.4316},
            {'command': self.iniciar3t, 'rely': 0.659},
            {'command': self.iniciarm35, 'rely': 0.885}
        ]

        for boton_jugar in botones_jugar:
            jugar_boton =   CTkButton(fondo, 
                         hover_color='#5a3c2b', fg_color='#704A35', bg_color='#e0c2b6',
                         text='Jugar', text_color='#ffffff', font=('TypoGraphica', 17),
                         corner_radius=0, width=619.1, height=63.8, command=boton_jugar['command'])
            jugar_boton.place(relx=0.2492,rely=boton_jugar['rely'], anchor='nw')
       
       
        self.contador = 0
        jugar_eastergg = CTkButton(self, 
                         hover_color= '#b66e3f',fg_color='#b66e34', bg_color='transparent',font=('TypoGraphica', 17),
                         corner_radius=0,
                         text='',
                         width=18, height=18,
                         command=self.generarEasterEgg)
        jugar_eastergg.place(relx=0.116,rely=0.162, anchor='nw')

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
        except PermissionError:
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
        self.T3_punt.configure(text = str(db.returnActivo()[4]))
        self.M35_punt.configure(text = str(db.returnActivo()[5]))
        print(db) # Mostramos los datos usando la sobrecarga del operador

    @staticmethod
    def instanciar_descripcion(funcion):
        """
        Instancia la descripción elegida

        Parámetros
        ----------
        funcion : function
            Función utilizada en el método wrapper() dentro de la función decorada
        """
        def wrapper(self):
            data = funcion(self)
            self.withdraw() # ocultamos el menú
            UiReglas(self, data['titulo'], imagen=data['imagen'], x=data['x'], y=data['y'],
                     hover_color=data['hover_color'],fg_color=data['fg_color']) 

        return wrapper
    
    @instanciar_descripcion    
    def descripcion_1T(self):
        """
        Muestra las reglas del juego 1T.
        """
        data = {'titulo': 'Reglas 1T', 
                'imagen': Image.open('./Imagenes/UI/Reglas/T1_r.png'), 
                'x':0.1, 'y': 0.8,
                'hover_color': '#3f4998', 'fg_color': '#5763c5'}
        return data
    
    @instanciar_descripcion
    def descripcion_2T(self):
        """
        Muestra las reglas del juego 2T.
        """
        data = {'titulo': 'Reglas 2T', 
                'imagen': Image.open('./Imagenes/UI/Reglas/T2_r.png'), 
                'x':0.1, 'y': 0.9,
                'hover_color': '#976042', 'fg_color': '#b97a57'}
        return data
    
    @instanciar_descripcion   
    def descripcion_3T(self):
        """
        Muestra las reglas del juego 3T.
        """
        data = {'titulo': 'Reglas 3T', 
                'imagen': Image.open('./Imagenes/UI/Reglas/T2_r.png'), 
                'x':0.1, 'y': 0.9,
                'hover_color': '#976042', 'fg_color': '#b97a57'}
        return data
        
    @instanciar_descripcion
    def descripcion_M35(self):
        """
        Muestra las reglas del juego M35.
        """
        data = {'titulo': 'Reglas M35', 
                'imagen': Image.open('./Imagenes/UI/Reglas/M35_r.png'), 
                'x':0.1, 'y': 0.85,
                'hover_color': '#f04e4e', 'fg_color': '#e04948'}
        return data
        
    @staticmethod
    def iniciar_juego(funcion):
        """
        Inicia el juego elegido.

        Parámetros
        ----------
        funcion : function
            Función utilizada en el método wrapper() dentro de la función decorada
        """
        def wrapper(self):
            self.withdraw() # ocultamos el menú
            self.quit()     # paramos temporalmente el mainloop(). 

            # Segunda iteración pantalla_actual está instanciada → elif == 'menu'
            try:
                self.master.main.pantalla_actual.cambio_pantalla = funcion(self)
            # Primera iteración pantalla_actual no está instanciada → 'Game' object has no attribute 'pantalla_actual' 
            except AttributeError: 
                self.master.main.juego_inicial = funcion(self)

        return wrapper

    @iniciar_juego
    def iniciar1t(self):
        """
        Inicia el juego 1T.
        """
        return 'seleccion_1t'
    @iniciar_juego
    def iniciar2t(self):
        """
        Inicia el juego 2T.
        """
        return '2t'   
    @iniciar_juego
    def iniciar3t(self):
        """
        Inicia el juego 3T.
        """
        return '3t'
    @iniciar_juego
    def iniciarm35(self):
        """
        Inicia el juego M35.
        """
        return 'm35'
    @iniciar_juego
    def iniciarEasterEgg(self):
        """
        Inicia el juego EasterEgg
        """
        self.generarPickle()
        return 'easter_egg'
    
    def generarEasterEgg(self):
        """
        Genera la inicialización del EasterEgg
        """
        self.contador += 1
        if self.contador == 3:
            self.contador = 0
            self.iniciarEasterEgg()

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
 
    def instanciarPartidas3T(self):
        """
        Instancia la UI(CTkTopLevel) que permite guardar/cargar partidas.
        El método es llamado en Pantallla (bucle) → self.cambio_pantalla == 'guardar-cargar'
        """
        
        PartidasGuardadas(master=self)