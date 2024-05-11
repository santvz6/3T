"""ui_login.py

Este fichero es el responsable de crear la interfaz de la ventana de inicio de sesión.

El fichero utiliza el módulo DataBase.py, situado dentro de la carpeta UI_db, el cual contiene el código encargado
de administrar la tabla de usuarios.

También utiliza la clase UiMenu del módulo ui_menu, situado dentro de la carpeta UI_db. Con esta clase se crea un
objeto ventana, que es la del menú principal.

Para utilizar el código, es necesaria la instalación de las librerías pillow y customtkinter en nuestro entorno virtual.

El fichero contiene únicamente la clase UiLogin, que hereda de CTk y es una clase con la que creamos la ventana
de inicio de sesión.
"""

from PIL import Image
from customtkinter import * # Documentación → https://customtkinter.tomschimansky.com/documentation/

# Para ejecutar código desde main
import UI_db.DataBase as db #  si ejecutamos el fichero desde aquí da error
                            # en cambio, desde main la ruta de los import esta perfecta
from UI_db.ui_menu import UiMenu

# ↓ Para pruebas en el fichero ↓
#import DataBase as db 
#from ui_menu import UiMenu


# UiLogin es la Ventana principal → Hereda de CTk
class UiLogin(CTk):
    """
    parent : CTk

    Crea un objeto ventana de inicio de sesión.

    Atributos
    ---------
    main : Game
        Instancia del juego.

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
    def __init__(self, main):   # main hace referencia a main.py
        """
        Inicializa la clase con el atributo especificado.

        También contiene todos los widgets de la ventana de inicio de sesión, así como

        Parámetros
        ----------
        main: Game
            Instancia del juego.
        """
        super().__init__()  # Inicializamos la superclase CTk (self hace referencia a CTk)
                            # Si no heredamos → master = CTk() → master.mainloop()

        #logo = Image.open('T1/Imagenes/TTT.png')
        #logo.save('T1/Imagenes/TTT.ico') # Transformar el logo en .ico usando Image de PIL
        self.iconbitmap('./Imagenes/UI/TTT.ico')

        self.geometry('800x600+500+120') # self representa CTk(), debido a que lo hemos heredado
        self.resizable(0,0)

        self.title('Inicio de Sesión / Crear Cuenta')
    
        self.main = main    # main.py, no podemos hacer import (circular import)


        ####    WIDGETS     ####
        fondo_img = CTkImage(Image.open('./Imagenes/UI/Login/log.png'), size=(800,600))
        fondo = CTkLabel(master = self, image=fondo_img, text="") 
        fondo.place(relx=0, rely=0, anchor='nw')

        bienvenida_foto = CTkImage(Image.open('./Imagenes/UI/Login/bienvenido.png'), size=(160,90))
        bienvenida = CTkLabel(master=self, image=bienvenida_foto, text="", bg_color='#eeeeed') 
        bienvenida.place(relx=0.37, rely=0.28, anchor='nw')

        usuario_foto_txt = CTkImage(Image.open('./Imagenes/UI/Login/usuario_txt.png'), size=(68,14))
        usuario_txt = CTkLabel(master=self, image=usuario_foto_txt, text="", bg_color='#eeeeed') 
        usuario_txt.place(relx=0.447, rely=0.465, anchor='nw')

        password_foto_txt = CTkImage(Image.open('./Imagenes/UI/Login/pasw_txt.png'), size=(80,18))
        password_txt = CTkLabel(master=self, image=password_foto_txt, text="", bg_color='#eeeeed') 
        password_txt.place(relx=0.44, rely=0.60, anchor='nw')

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

        login_boton = CTkButton(master=fondo, width=100, height=20,
                                text='Iniciar sesión', text_color='#000000',
                                bg_color='#eeeeed', fg_color='#cecece',
                                hover_color='#ababab', font=('Bahnschrift',12),
                                corner_radius=5,
                                border_width=1.5, border_color='#c1c1c1',
                                command=self.boton_inicio_sesion)
        login_boton.place(relx=0.5, rely= 0.76, anchor='center')

        register_boton = CTkButton(master=fondo, width=100, height=20,
                                text='Crear cuenta', text_color='#000000',
                                bg_color='#eeeeed', fg_color='#cecece',
                                hover_color='#ababab', font=('Bahnschrift',12),
                                corner_radius=5,
                                border_width=1.5, border_color='#c1c1c1',
                                command=self.boton_crear_cuenta)
        register_boton.place(relx=0.5, rely= 0.83, anchor='center')

        self.protocol("WM_DELETE_WINDOW", self.on_closing) # si le damos a la x de cerrar
    
    def on_closing(self):
        """
        Para el programa cuando se cierra la ventana manualmente.
        """
        sys.exit()

    # Se ejecuta cuando se presiona el botón (command = boton_inicio_sesión)
    def boton_inicio_sesion(self):
        usuario = self.usuario_inp.get('0.0', 'end')[:-1]   # especificamos que trozo de la TextBox agarramos (inicio: 0.0, fin: end)
        contraseña = self.passw_inp.get('0.0', 'end')[:-1]  # usando esta configuración siempre se nos guardará un caracter final de espacio extra
                                                            # por tanto usaremos [:-1], para agarrar todos menos el último
        if db.buscar_usuario(str(usuario), str(contraseña)) == 1 :  # 1: encontró una persona que coincide con los datos
            db.set_activo(usuario) # le establecemos como activo

            self.withdraw() # ocultamos la pantalla principal
            # Lo ocultamos ya que si destruimos la ventana (self.destroy()), .mainloop() se detiene
            # https://stackoverflow.com/questions/77975424/customtkinter-invalid-command-name

            self.menu = UiMenu(self) # instanciamos el menu (pantalla secundaria)

        else:
            pass # ya hemos hecho print('Usuario inexistente') en la data base
            
    # Se ejecuta cuando se presiona el botón (command = boton_crear_cuenta)
    def boton_crear_cuenta(self):
        """
        Crea un nuevo usuario con los datos introducidos, si no existe uno ya, cuando se hace click en el botón de crear
        cuenta. Comprueba los datos y los introduce importando la tabla de usuarios del script DataBase.py.
        """
        usuario = self.usuario_inp.get('0.0', 'end')[:-1]
        contraseña = self.passw_inp.get('0.0', 'end')[:-1]
        if db.buscar_usuario(usuario, contraseña) == -1: # si es -1 no se econtró a nadie → creamos el usuario
            db.insertarUsuario(usuario, contraseña) # creamos el usuario / lo insertamos en la data base
            db.set_activo(usuario) # ponemos activo al nuevo usuario

            self.withdraw() # ocultamos la pantalla principal

            self.menu = UiMenu(self)    # instanciamos el menu (pantalla secundaria)
            
                                        # recibe como parámetro master = CTk() → la superclase (ventana principal)


        else: # en el caso de return = 0 o 1, el usuario ya existe
            print('Usuario existente') # Imprimimos por terminal que ya existe
                                       # no destruimos la pantalla aún

    #def menu(self):
        # OTRA FORMA DE HACER EL MENÚ (DENTRO DEL MISMO FICHERO)
        #self.menu = CTkToplevel()
        #self.menu.title('HOLA')
        # ...
