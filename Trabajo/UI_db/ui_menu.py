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
        
        #print(CTkToplevel.__bases__) # Para ver de donde hereda CTkTopLevel

        self.title('TTT')
        self.geometry('1280x720+200+40')
        self.resizable(0,0)

        # ↓ Creación de widgets ↓ #

        ### --- Fondo del menú --- ###
        img_menu = CTkImage(Image.open('T1/Imagenes/Menu/menu.png'), size=(1280,720)) # la abrimos con PIL dentro de un CTkImage 
        fondo = CTkLabel(master=self, image=img_menu, text='')  # mostramos la foto en una etiqueta
        fondo.place(relx=0, rely=0, anchor='nw')

        ### --- Foto de Usuario --- ###
        foto_usuario_db = db.return_activo()[1] # devolvemos la foto guardada en la base de datos
        foto_usuario_pil = CTkImage(Image.open(foto_usuario_db), size=(200,200)) # la abrimos con PIL dentro de un CTkImage 
        self.foto_cuadro = CTkLabel(self, image=foto_usuario_pil, text='')  # mostramos la foto en una etiqueta
        self.foto_cuadro.place(relx=0.88, rely=0.3, anchor='center')             # blit en la pantalla 

    
        boton_foto = CTkButton(self, width=160, height=30, 
                            fg_color='#ede1d5', hover_color= '#c8beb4', bg_color = '#fceee2',
                            text='Cambiar foto', font=('typoGraphica',17), text_color='#a2857a', 
                            command=self.cambiar_foto)
        boton_foto.place(relx=0.88, rely=0.48,anchor='center')


        ### --- Estadísticas --- ###
        cuadro = CTkButton(self, border_width=2, text='', width=200, height=300,
                           border_color='#ede1d5', fg_color= '#fceee2', bg_color='#fceee2' , hover_color='#fceee2')
        cuadro.place(relx=0.88, rely=0.74,anchor='center')

        estadisticas_txt = CTkLabel(self, text='Estadisticas', font=('typoGraphica',18), text_color='#a2857a', bg_color='#fceee2')
        estadisticas_txt.place(relx=0.88, rely=0.56,anchor='center')

        # T1
        T1_txt = CTkLabel(self, text='T1', font=('typoGraphica',18), text_color='#a2857a', bg_color='#fceee2')
        T1_txt.place(relx=0.88, rely=0.62,anchor='center')

        Victorias_txt = CTkLabel(self, text='Victorias:    3', font=('typoGraphica',18), text_color='#a2857a', bg_color='#fceee2')
        Victorias_txt.place(relx=0.88, rely=0.65,anchor='center')
        


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