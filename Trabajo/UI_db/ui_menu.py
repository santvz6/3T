from customtkinter import *
from CTkTable import CTkTable
from PIL import Image, ImageTk  # Image para abrir imagenes dentro del proyecto
                                # ImageTK para imagenes mediante un path


# Para código desde main
import UI_db.DataBase as db #  si ejecutamos el fichero desde aquí da error
                            # en cambio, desde main la ruta de los import esta perfecta


# Para pruebas en el fichero
#import DataBase as db 


# UiMenu es la ventana secundaria
# Por eso heredamos CTkToplevel
class UiMenu(CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master) # le damos al valor del master heredado, 
                                        # el master de la clase UILogin (ventana principal)
                                        # de esta forma mostramos por la pantalla (master)
                                        # esta ventana secundaria
        
        self.geometry('1280x720+200+40')
  
        # ↓ Creación de widgets ↓ #

        lateral_izq = CTkFrame(master=self, fg_color="#ccae89",  width=340, height=720, corner_radius=0)
        lateral_izq.pack_propagate(0) # desactivamos la propagación de tamaño si se añaden widgets
        lateral_izq.pack(fill="y", anchor="w", side="left")


        nom_proyecto = CTkLabel(master=lateral_izq, text='The Terrorist\nTeam', font=('TypoGraphica', 40), 
                        fg_color='transparent', text_color='#FFFFFF')
        nom_proyecto.place(relx=0.5, rely=0.2, anchor='center')


        ### --- 1T --- ###
        t1_foto = CTkImage(light_image=Image.open('T1/Imagenes/menu1T.png'), dark_image=Image.open('T1/Imagenes/menu1T.png'), size=(120,120))
        t1_cuadro = CTkLabel(self, image=t1_foto, text="") 
        t1_cuadro.place(relx=0.40, rely=0.08, anchor='nw') # anchor = nortwest

        boton_t1 = CTkButton(master=self, width=120, height=40, fg_color='#e5decc', text='PLAY',font=('typoGraphica',17),hover_color= '#a59d89', text_color='#54492d')
        boton_t1.place(relx=0.53, rely=0.19,anchor='nw')

        text_t2 =  CTkLabel(self, text='Un juego donde el\nunico limite es tu  mente.', font=('typoGraphica',12),justify='left') 
        text_t2.place(relx=0.53, rely=0.12,anchor='nw')

        ### --- 2T --- ###
        t2 = CTkImage(light_image=Image.open('T1/Imagenes/menu2T.png'), dark_image=Image.open('T1/Imagenes/menu2T.png'), size=(120,120))
        t2_cuadro = CTkLabel(self, image=t2, text="") 
        t2_cuadro.place(relx=0.40, rely=0.31, anchor='nw')

        boton_t2 = CTkButton(master=self, width=120, height=40, fg_color='#f3b816', text='PLAY',font=('typoGraphica',17),hover_color= '#c99811')
        boton_t2.place(relx=0.53, rely=0.42,anchor='nw')

        text_t2 =  CTkLabel(self, text='Un juego donde el\nunico limite es tu  mente.', font=('typoGraphica',12),justify='left') 
        text_t2.place(relx=0.53, rely=0.35,anchor='nw')


        ### --- 3T --- ###
        t3 = CTkImage(light_image=Image.open('T1/Imagenes/menu3T.png'), dark_image=Image.open('T1/Imagenes/menu3T.png'), size=(120,120))
        t3_cuadro = CTkLabel(self, image=t3, text="")  
        t3_cuadro.place(relx=0.40, rely=0.53, anchor='nw')

        boton_t3 = CTkButton(master=self, width=120, height=40, fg_color='#7d24bd', text='PLAY',font=('typoGraphica',17),hover_color= '#6d1fa6')
        boton_t3.place(relx=0.53, rely=0.64,anchor='nw')

        text_t3 =  CTkLabel(self, text='Un juego donde el\nunico limite es tu  mente.', font=('typoGraphica',12),justify='left') 
        text_t3.place(relx=0.53, rely=0.57,anchor='nw')

        ### --- Foto de Usuario --- ###
        foto_usuario_db = db.return_activo()[1] # devolvemos la foto guardada en la base de datos
        
        foto_usuario_pil = CTkImage(Image.open(foto_usuario_db), size=(200,200)) # la abrimos con PIL dentro de un CTkImage 
        self.foto_cuadro = CTkLabel(self, image=foto_usuario_pil, text='')  # mostramos la foto en una etiqueta
        self.foto_cuadro.place(relx=0.9, rely=0.2, anchor='center')             # blit en la pantalla 

    
        boton_foto = CTkButton(master=self, width=120, height=40, fg_color='#FFFFFF', text='FOTO',
                        font=('typoGraphica',17),hover_color= '#DDDDDD', command=self.cambiar_foto, text_color='#000000')
        boton_foto.place(relx=0.9, rely=0.4,anchor='center')


    def cambiar_foto(self):
        # se ejecuta al hacer click en el botón → cambiar foto
            
            foto_nueva = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")])
            usuario_activo = db.return_activo()[0] # devolvemos el nombre
       
            # Puede ocurrir un error si al ejecutar filedialog.askopenfilename
            # no se selecciona ninguna foto, en vez de dejar la foto del usuario en la DB vacía
            # mantenemos la foto anterior para que no de problemas más adelante
            try:
                foto_usuario_pil = CTkImage(Image.open(foto_nueva), size=(200,200)) # la abrimos con PIL dentro de un CTKImage
                                                                                    # puede dar error si no tenemos una ruta
                                                                                    # ocurre si el usuario cierra filedialog
                db.update_db(usuario_activo, {'FOTO':foto_nueva}) # si no da fallos, la foto se actualiza en la db
            
            except:
                foto_usuario_pil = CTkImage(Image.open(db.return_activo()[1]), size=(200,200))  # la foto a actualizar será la misma
                print('Excepción: No se seleccionó ninguna foto')                               # que el usuario tenía en la db
            
            self.foto_cuadro.configure(image = foto_usuario_pil) # hacemos el update de la foto aquí 