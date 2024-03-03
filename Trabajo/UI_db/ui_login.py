from customtkinter import *
from PIL import Image

# Para código desde main
import UI_db.DataBase as db #  si ejecutamos el fichero desde aquí da error
                            # en cambio, desde main la ruta de los import esta perfecta
from UI_db.ui_menu import UiMenu

# Para pruebas en el fichero
#import DataBase as db 
#from ui_menu import UiMenu


#db.update_db('s',{'FOTO':filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")])})

# UiLogin es la Ventana principal
class UiLogin(CTk):
    def __init__(self):
        super().__init__() # Heredamos de CTk: master (la superficie de la pantalla)

        self.geometry('800x600+500+120') 
        self.resizable(0,0)
        
        fondo_img = CTkImage(light_image=Image.open('T1/Imagenes/login/log.png'), dark_image=Image.open('T1/Imagenes/login/log.png'), size=(800,600))
        fondo = CTkLabel(master = self, image=fondo_img, text="") 
        fondo.place(relx=0, rely=0, anchor='nw')

        bienvenida_foto = CTkImage(Image.open('T1/Imagenes/login/bienvenido.png'), size=(160,90))
        bienvenida = CTkLabel(master=self, image=bienvenida_foto, text="", bg_color='#eeeeed') 
        bienvenida.place(relx=0.37, rely=0.28, anchor='nw')

        usuario_foto_txt = CTkImage(Image.open('T1/Imagenes/login/usuario_txt.png'), size=(68,14))
        usuario_txt = CTkLabel(master=self, image=usuario_foto_txt, text="", bg_color='#eeeeed') 
        usuario_txt.place(relx=0.447, rely=0.465, anchor='nw')

        password_foto_txt = CTkImage(Image.open('T1/Imagenes/login/pasw_txt.png'), size=(80,18))
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

    # Se ejecuta cuando se presiona el botón (command = boton_inicio_sesión)
    def boton_inicio_sesion(self):
        usuario = self.usuario_inp.get('0.0', 'end')[:-1]   # especificamos que trozo de la TextBox agarramos (inicio: 0.0, fin: end)
        contraseña = self.passw_inp.get('0.0', 'end')[:-1]  # usando esta configuración siempre se nos guardará un caracter final de espacio extra
                                                            # por tanto usaremos [:-1], para agarrar todos menos el último
        if db.buscar_usuario(str(usuario), str(contraseña)) == 1 :  # 1: encontró una persona que coincide con los datos
            db.set_activo(usuario) # le establecemos como activo

            self.withdraw() # ocultamos la pantalla principal
            # https://stackoverflow.com/questions/77975424/customtkinter-invalid-command-name

            UiMenu(self) # instanciamos el menu (pantalla secundaria)
            
        else:
            pass # ya hemos hecho print('Usuario inexistente') en la data base
            
    # Se ejecuta cuando se presiona el botón (command = boton_crear_cuenta)
    def boton_crear_cuenta(self):
        usuario = self.usuario_inp.get('0.0', 'end')[:-1]
        contraseña = self.passw_inp.get('0.0', 'end')[:-1]
        if db.buscar_usuario(usuario, contraseña) == -1: # si es -1 no se econtró a nadie → creamos el usuario
            db.insertarUsuario(usuario, contraseña) # creamos el usuario / lo insertamos en la data base
            db.set_activo(usuario) # ponemos activo al nuevo usuario

            self.withdraw()

            UiMenu(self) # instanciamos el menu (pantalla secundaria)


        else: # en el caso de return = 0 o 1, el usuario ya existe
            print('Usuario existente') # Imprimimos por terminal que ya existe
                                       # no destruimos la pantalla aún
