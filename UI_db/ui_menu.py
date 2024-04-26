from customtkinter import *
from CTkTable import CTkTable
from PIL import Image, ImageTk  # Image para abrir imagenes dentro del proyecto
                                # ImageTK para imagenes mediante un path

from UI_db.ui_reglas import UiReglas

# Para código desde main
import UI_db.DataBase as db #  si ejecutamos el fichero desde aquí da error
                            # en cambio, desde main la ruta de los import esta perfecta

# Para el fichero del Easter Egg
import pickle

# Para pruebas en el fichero
#import DataBase as db 



# UiMenu es la ventana secundaria
# Por eso heredamos CTkToplevel
class UiMenu(CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master) # le damos al valor del master heredado, 
                                        # el master de la clase superior(UILogin / ventana principal)
                                        # de esta forma estaríamos usando el CTk().mainloop
                                        # para ventanas secundarias
        
        #print(CTkToplevel.__bases__) # Para ver de dónde hereda CTkTopLevel

        self.title('TTT')
        self.geometry('1280x720+200+40')
        self.resizable(0,0)

        # https://stackoverflow.com/questions/75825190/how-to-put-iconbitmap-on-a-customtkinter-toplevel
        # En un foro de stackoverflow se menciona que trabajar con iconbitmap cuando se hereda de TopLevel
        # ocasiona problemas debido a que customtkinter cambia la foto del icono a las 250 milésimas de heredar.
        self.after(250, lambda: self.iconbitmap(('./Imagenes/UI/TTT.ico')))


        # ↓ Creación de widgets ↓ #

        ### --- Fondo del menú --- ###
        img_menu = CTkImage(Image.open('./Imagenes/UI/Menu/menu.png'), size=(1280,720)) # la abrimos con PIL dentro de un CTkImage 
        fondo = CTkLabel(master=self, image=img_menu, text='')  # mostramos la foto en una etiqueta
        fondo.place(relx=0, rely=0, anchor='nw')

        ### --- Foto de Usuario --- ###
        foto_usuario_db = db.return_activo()[1] # devolvemos la foto guardada en la base de datos

        # Se produce cuando el usuario tenía una foto de perfil
        # que ha sido borrada de su ordenador
        try:
            foto_usuario_pil = CTkImage(Image.open(foto_usuario_db), size=(200,200)) # la abrimos con PIL dentro de un CTkImage 
        except:
            print('Foto borrada')
            foto_usuario_pil = CTkImage(Image.open('./Imagenes/UI/Menu/foto_default.jpeg'), size=(200,200))

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
                                text = str(db.return_activo()[2]), text_color='#a2857a', font=('TypoGraphica', 18))
                                
        self.T1_punt.place(relx=0.88, rely=0.65,anchor='center')

        # T2
        T2_txt = CTkLabel(self, text='T2', font=('TypoGraphica', 18), text_color='#a2857a', bg_color='#fceee2')
        T2_txt.place(relx=0.88, rely=0.7,anchor='center')

        self.T2_punt = CTkLabel(self, bg_color='#fceee2',
                                text = str(db.return_activo()[3]), text_color='#a2857a', font=('TypoGraphica', 18))
                                
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
        bm_d = CTkButton(fondo, 
                         hover_color='#976042', fg_color='#b97a57', bg_color='#e0c2b6',font=('TypoGraphica', 17),
                         corner_radius=0,
                         text='Informacion', text_color='#ffffff', #a2857a
                         width=619.1, height=43.78)
        bm_d.place(relx=0.2492,rely=0.8036, anchor='nw')

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
                         command=self.easter_egg)
        b_eg.place(relx=0.116,rely=0.162, anchor='nw')
        self.contador = 0

        self.protocol("WM_DELETE_WINDOW", self.on_closing) # si le damos a la x de cerrar
    
    def on_closing(self):
        sys.exit()


############################### FUNCIONES ###############################
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
    
    def actualizar_punt(self):
        self.T1_punt.configure(text = str(db.return_activo()[2]))
        self.T2_punt.configure(text = str(db.return_activo()[3]))


    def descripcion_1T(self):
        self.withdraw() # ocultamos la pantalla menú
        imagen = Image.open('./Imagenes/UI/Reglas/T1_r.png')
        UiReglas(self, 'Reglas T1', imagen=imagen, hover_color='#3f4998',fg_color='#5763c5',x=0.1,y=0.8) # le damos como argumento la instancia de UiMenu a UiT1
    def descripcion_2T(self):
        imagen = Image.open('./Imagenes/UI/Reglas/T2_r.png')
        self.withdraw() # ocultamos la pantalla menú
        UiReglas(self, 'Reglas 21', imagen=imagen, hover_color='#976042',fg_color='#b97a57',x=0.1,y=0.9) # le damos como argumento la instancia de UiMenu a UiT1
        

    def t1(self):
        self.juego_elegido = '1t'
        self.iniciar_juego(self.juego_elegido)
    def t2(self):
        self.juego_elegido = '2t'
        self.iniciar_juego(self.juego_elegido)
    def t3(self):
        self.juego_elegido = '3t'
        self.iniciar_juego(self.juego_elegido)
    def m35(self):
        self.juego_elegido = 'm35'
        self.iniciar_juego(self.juego_elegido)

    
    def iniciar_juego(self, juego_elegido:str):
        self.withdraw() # ocultamos el menú
        self.quit()     # paramos temporalmente el mainloop(). En Pantalla se activa → elif == 'menu'
        self.master.main.juego_inicial = juego_elegido   # Sólo nos servirá al entrar en el primer juego, lo usamos
                                                # porque Pantalla no está instanciado al inicio de main.py
        try:
            self.master.main.pantalla_actual.cambio_pantalla = juego_elegido #en las restantes vueltas, Pantalla está instanciada
        except:
            #print('Primera vuelta del bucle')
            pass   
        


    def easter_egg(self):
        self.contador += 1
        if self.contador == 3:
            self.contador = 0
            self.withdraw() # ocultamos el menú
            self.quit()     # paramos temporalmente el mainloop(). En Pantalla se activa → elif == 'menu'

            # Comprobamos si hay datos existentes
            try:
                pickle_reader = open('easter_egg_score.pkl', 'rb')

            except:
                with open('easter_egg_score.pkl','wb') as pickle_writer:  # En caso de que no exista el fichero, se crea
                    pickle.dump(                                          # y se introduce el diccionario con el usuario
                        {
                            'PERSONAL_HIGH_SCORES': {db.return_activo()[0]: 0},
                            'GLOBAL_HIGH_SCORE': 0
                        }, pickle_writer)

            else:
                scores = pickle.load(pickle_reader)
                if db.return_activo()[0] not in scores['PERSONAL_HIGH_SCORES'].keys():  # Si existe, comprueba si hay
                    scores['PERSONAL_HIGH_SCORES'][db.return_activo()[0]] = 0           # datos del usuario actual
                pickle_reader.close()

                pickle_writer = open('easter_egg_score.pkl', 'wb')  # Actualizamos los datos
                pickle.dump(scores, pickle_writer)
                pickle_writer.close()

            self.master.main.juego_inicial = 'easter_egg'   # Sólo nos servirá al entrar en el primer juego, lo usamos
                                                            # porque Pantalla no está instanciado al inicio de main.py

            try:
                self.master.main.pantalla_actual.cambio_pantalla = 'easter_egg' #en las restantes vueltas, Pantalla está instanciada

            except:
                #print('Primera vuelta del bucle')
                pass
