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
    '''
    
    
    '''
    def __init__(self, main):  
        super().__init__()  # Inicializamos la superclase CTk (self hace referencia a CTk)
                            # Si no heredamos → master = CTk() → master.mainloop()

        self.main = main

        #logo = Image.open('T1/Imagenes/TTT.png')   
        #logo.save('T1/Imagenes/TTT.ico') # Transformar el logo en .ico usando Image de PIL
        self.iconbitmap('./Imagenes/UI/TTT.ico')

        self.geometry('800x600+500+120') # self representa CTk(), debido a que lo hemos heredado
        self.resizable(0,0)

        self.title('Inicio de Sesión / Crear Cuenta')
    


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
        sys.exit()

    # Se ejecuta cuando se presiona el botón (command = boton_inicio_sesión)
    def boton_inicio_sesion(self):
        usuario = self.usuario_inp.get('0.0', 'end')[:-1]   # especificamos que trozo de la TextBox agarramos (inicio: 0.0, fin: end)
        contraseña = self.passw_inp.get('0.0', 'end')[:-1]  # usando esta configuración siempre se nos guardará un caracter final de espacio extra
                                                            # por tanto usaremos [:-1], para agarrar todos menos el último
        if db.buscarUsuario(str(usuario), str(contraseña)) == 1 :  # 1: encontró una persona que coincide con los datos
            db.setActivo(usuario) # le establecemos como activo

            self.withdraw() # ocultamos la pantalla principal
            # Lo ocultamos ya que si destruimos la ventana (self.destroy()), .mainloop() se detiene
            # https://stackoverflow.com/questions/77975424/customtkinter-invalid-command-name

            print(db)
            self.menu = UiMenu(self) # instanciamos el menu (pantalla secundaria)

        else:
            pass # ya hemos hecho print('Usuario inexistente') en la data base
            
    # Se ejecuta cuando se presiona el botón (command = boton_crear_cuenta)
    def boton_crear_cuenta(self):
        usuario = self.usuario_inp.get('0.0', 'end')[:-1]
        contraseña = self.passw_inp.get('0.0', 'end')[:-1]
        if db.buscarUsuario(usuario, contraseña) == -1: # si es -1 no se econtró a nadie → creamos el usuario
            print(f'Usuario "{usuario}" registrado')
            db.insertarUsuario(usuario, contraseña) # creamos el usuario / lo insertamos en la data base
            db.setActivo(usuario) # ponemos activo al nuevo usuario

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
