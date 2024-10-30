""" ui_login.py

Este fichero es el responsable de crear la interfaz de la ventana de inicio de sesión.
Nuestra clase UiLogin hereda de CTk para así poder establecer una ventana principal.

El fichero utiliza los módulos:

* UI_db.DataBase:  contiene el código encargado de administrar la tabla de usuarios.
* UI_db.ui_menu: la instanica de esta clase conlleva la creación de una venta secundaria que hereda de CTkToplevel

Para utilizar el código es necesaria la instalación de las siguientes librerías en nuestro entorno virtual:
 * pillow: utilizado para el tratamiento de imagenes
 * customtkinter: utilizado para la interfaz

También utilizamos las librerías incorporadas en Python:
 * sys: utilizado para salir del programa

Documentación: 
CTk: https://customtkinter.tomschimansky.com/documentation/
"""

# Librerías
from PIL import Image
from customtkinter import *
import sys

# Ficheros
from UI_db.DataBase import db_principal as db 
from UI_db.ui_menu import UiMenu

class UiLogin(CTk):
    """
    UiLogin crea la ventana principal heredando de la clase CTk. En esta ventana se mostrará
    la UI de la pantalla Login donde el usuario podrá iniciar sesión/registrarse.

    parent : CTk
        Crea un objeto de ventana principal

    
    Métodos
    -------
    __init__(self, main)
        Inicializa la clase con el atributo especificado.
    on_closing(self)
        Deja de ejecutar el programa cuando se cierra la ventana manualmente.
    boton_inicio_sesion(self)
        Comprueba si el usuario existe en la base de datos al hacer click en el botón de iniciar sesión.
    boton_crear_cuenta(self)
        Crea un nuevo usuario con los datos introducidos, si no existe uno ya, cuando se hace click en el botón de crear
        cuenta.
    """

    def __init__(self, main):  
        """
        Inicializa la clase con el atributo especificado.

        Atributos
        ---------
        main : Game
            Representa todos los atributos de la clase Game
        """
        # No hace falta instanciar CTk manualmente
        # root = CTk()
        super().__init__() 
        
        self.main = main

        # Establecer icono
        try:
            Image.open('./Imagenes/UI/TTT.ico') 
        except FileNotFoundError:
            print('Intentando crear logo.ico')
            try:
                logo = Image.open('./Imagenes/UI/TTT.png')   
            except FileNotFoundError:
                print('No se encontró ningún logo.png')
            else:
                logo.save('./Imagenes/UI/TTT.ico') 
                self.iconbitmap('./Imagenes/UI/TTT.ico')
                print('Icono.ico creado con éxito')
        else:
            self.iconbitmap('./Imagenes/UI/TTT.ico')

        # Establecer Tamaño - Posición - Reescalado
        self.geometry('800x600+500+120')
        self.resizable(0,0)
        
        # Establecer título
        self.title('Inicio de Sesión / Crear Cuenta')
    
######################       WIDGETS        #####################
    
    ### IMAGENES
        fondo_img = CTkImage(Image.open('./Imagenes/UI/Login/log.png'), size=(800,600))
        fondo = CTkLabel(master = self, image=fondo_img, text="") 
        fondo.place(relx=0, rely=0, anchor='nw')

        bienvenida_foto = CTkImage(Image.open('./Imagenes/UI/Login/bienvenido.png'), size=(160,90))
        bienvenida = CTkLabel(master=self, image=bienvenida_foto, text="", bg_color='#eeeeed') 
        bienvenida.place(relx=0.37, rely=0.28, anchor='nw')

        usuario_txt_img = CTkImage(Image.open('./Imagenes/UI/Login/usuario_txt.png'), size=(68,14))
        usuario_txt = CTkLabel(master=self, image=usuario_txt_img, text="", bg_color='#eeeeed') 
        usuario_txt.place(relx=0.447, rely=0.465, anchor='nw')

        password_txt_img = CTkImage(Image.open('./Imagenes/UI/Login/pasw_txt.png'), size=(80,18))
        password_txt = CTkLabel(master=self, image=password_txt_img, text="", bg_color='#eeeeed') 
        password_txt.place(relx=0.44, rely=0.60, anchor='nw')

    ### TEXTBOX
        self.usuario_inp = CTkTextbox(master=fondo,width=160,height=20, # usamos self para llamarlo en las funciones
                        border_width=1.5, border_color='#c1c1c1',       # boton_inicio_sesion() y boton_crear_usuario 
                        fg_color='#cecece', bg_color='#eeeeed',
                        text_color='#000000')
        self.usuario_inp.place(relx=0.5, rely=0.54, anchor = 'center')

        self.passw_inp = CTkTextbox(master=fondo,width=160,height=20,  # usamos self para llamarlo en las funciones
                        border_width=1.5, border_color='#c1c1c1',      # boton_inicio_sesion() y boton_crear_usuario 
                        fg_color='#cecece', bg_color='#eeeeed',
                        text_color='#000000')
        self.passw_inp.place(relx=0.5, rely=0.68, anchor = 'center')
    
    ### BOTONES
        login_boton = CTkButton(master=fondo, width=100, height=20,
                                text='Iniciar sesión', text_color='#000000',
                                bg_color='#eeeeed', fg_color='#cecece',
                                hover_color='#ababab', font=('Bahnschrift',12),
                                corner_radius=5,
                                border_width=1.5, border_color='#c1c1c1',
                                command=self.boton_inicio_sesion)       # command: inicio de sesión
        login_boton.place(relx=0.5, rely= 0.76, anchor='center')

        register_boton = CTkButton(master=fondo, width=100, height=20,
                                text='Crear cuenta', text_color='#000000',
                                bg_color='#eeeeed', fg_color='#cecece',
                                hover_color='#ababab', font=('Bahnschrift',12),
                                corner_radius=5,
                                border_width=1.5, border_color='#c1c1c1',
                                command=self.boton_crear_cuenta)        # command: crear cuenta
        register_boton.place(relx=0.5, rely= 0.83, anchor='center')
    
    ### ERIQUETAS
        self.advertencia = CTkLabel(fondo, width=240,height=30, 
                                text_color='#000000', text='Inicia sesión / Crea una cuenta',
                                font=('Bahnschrift',13), bg_color='#eeefee')
        self.advertencia.place(relx=0.5, rely=0.94, anchor='center')
                                    
        # EQUIVALENTE A → event.type == pg.QUIT 
        self.protocol("WM_DELETE_WINDOW", self.finalizar_UI) # llama al método finalizar_UI()
    
    ######################       MÉTODOS DE ACTUALIZACIÓN        #####################
    def finalizar_UI(self):
        """
        Finaliza el programa.
        """
        sys.exit()

    def boton_inicio_sesion(self):
        """
        Para iniciar sesión comprueba los datos usando el método de la DataBase llamado buscarUsuario y si lo encuentra
        lo establece como activo usando el método setActivo.
        """

        usuario = self.usuario_inp.get('0.0', 'end')[:-1]   # especificamos que trozo de la TextBox agarramos (inicio: 0.0, fin: end)
        contraseña = self.passw_inp.get('0.0', 'end')[:-1]  # usando esta configuración siempre se nos guardará un caracter final de espacio extra
                                                            # por tanto usaremos [:-1], para agarrar todos menos el último
        
        busqueda = db.buscarUsuario(str(usuario), str(contraseña))  # 1: encontró una persona que coincide con los datos
                                                                    # 0: encontró el usuario pero la contraseña no coincide
                                                                    # -1: no encontró al usaurio
       
        if  busqueda == 1 :  
            db.setActivo(usuario)

            self.withdraw() # ocultamos la pantalla principal
            # Lo ocultamos ya que si destruimos la ventana, usando self.destroy(), .mainloop() se detiene.
            # https://stackoverflow.com/questions/77975424/customtkinter-invalid-command-name

            print(db) # Información del usuario usando la sobrecarga del operador
            self.menu = UiMenu(self)    # instanciamos el menu (pantalla secundaria)
                                        # como argumento recibe el objeto CTk (self)
        elif busqueda == 0:
            self.advertencia.configure(text='Contraseña incorrecta')
        else:
            self.advertencia.configure(text=f'El Usuario {usuario} no está registrado')     

    def boton_crear_cuenta(self):
        """
        Crea un nuevo usuario, si no existe uno ya, con los datos introducidos en el widget self.usuario_inp y self.passw_inp.
        Este proceso se realiza con los métodos de la DataBase: buscarUsuario y setActivo.
        
        """
        usuario = self.usuario_inp.get('0.0', 'end')[:-1]
        contraseña = self.passw_inp.get('0.0', 'end')[:-1]

        # -1: no se econtró a nadie → creamos el usuario 
        if db.buscarUsuario(usuario, contraseña) == -1:           
            db.insertarUsuario(usuario, contraseña) # creamos el usuario / lo insertamos en la data base
            db.setActivo(usuario)
            self.withdraw()
            print(f'Usuario "{usuario}" registrado')
            self.menu = UiMenu(self)    
        else: 
            self.advertencia.configure(text='El usuario ya existe')
