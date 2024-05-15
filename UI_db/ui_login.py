""" ui_login.py

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
from UI_db.DataBase import db_principal as db #  si ejecutamos el fichero desde aquí da error
                            # en cambio, desde main la ruta de los import esta perfecta
from UI_db.ui_menu import UiMenu

# ↓ Para pruebas en el fichero ↓
#import DataBase as db 
#from ui_menu import UiMenu


# UiLogin es la Ventana principal → Hereda de CTk
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
        super().__init__()  
        # Al heredar de CTk obtenemos todos los atributos de esta clase (usamos self)
        # Como segunda opción podríamos instanciar la Clase CTk y trabajar con ella de la siguiente forma:
        # master = CTk()
        # ...
        # master.inconbitmap()

        # Atributos
        self.main = main


        # Ajustes CTk

        # Establecer icono
        try:
            Image.open('./Imagenes/UI/TTT.png') 
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
        self.geometry('800x600+500+120') # self representa CTk(), debido a que lo hemos heredado
        self.resizable(0,0)

        # Establecer título
        self.title('Inicio de Sesión / Crear Cuenta')
    
        ######################       WIDGETS        #####################
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
        
        # 1: encontró una persona que coincide con los datos
        if db.buscarUsuario(str(usuario), str(contraseña)) == 1 :  
            db.setActivo(usuario)

            self.withdraw() # ocultamos la pantalla principal
            # Lo ocultamos ya que si destruimos la ventana, usando self.destroy(), .mainloop() se detiene.
            # https://stackoverflow.com/questions/77975424/customtkinter-invalid-command-name

            print(db) # Información del usuario usando la sobrecarga del operador
            self.menu = UiMenu(self)    # instanciamos el menu (pantalla secundaria)
                                        # como argumento recibe el objeto CTk (self)
            
    # Se ejecuta cuando se presiona el botón (command = boton_crear_cuenta)
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
            self.menu = UiMenu(self)    # instanciamos el menu (pantalla secundaria)          
                                        # recibe como parámetro master = CTk() → la superclase (ventana principal)
        else: 
            print('Usuario existente')
                                       
    # Si en la clase Menu no heredamos de CTkTopLevel habría que instanciar CTkTopLevel()  
    #def menu(self):    
        #self.menu = CTkToplevel()
        #self.menu.title('HOLA')
        # ...