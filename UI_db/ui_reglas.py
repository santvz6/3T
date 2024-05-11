from customtkinter import *

# ui_t1 es una ventana secundaria
# Por eso heredamos CTkToplevel

class UiReglas(CTkToplevel):
    def __init__(self, master, title:str, imagen, 
                 hover_color:str, fg_color:str,
                 x:int, y:int):
        super().__init__(master=master) # damos una referencia de la 
                                        # ventana 'principal'(UiMenu) a la clase 
                                        # padre CTkTopLevel
        
        #print(CTkToplevel.__bases__) # Para ver ºe donde hereda CTkTopLevel

        self.title(title)
        self.geometry('1280x720+200+40')
        self.resizable(0,0)

        # https://stackoverflow.com/questions/75825190/how-to-put-iconbitmap-on-a-customtkinter-toplevel
        # En un foro de stackoverflow se menciona que trabajar con iconbitmap cuando se hereda de TopLevel
        # ocasiona problemas debido a que customtkinter cambia la foto del icono a las 250 milésimas de heredar.
        self.after(250, lambda: self.iconbitmap(('./Imagenes/UI/TTT.ico')))

        fondo_img = CTkImage(imagen, size=(1280,720)) # la abrimos con PIL dentro de un CTkImage 
        fondo = CTkLabel(self, image=fondo_img, text='', bg_color='#fceee2')  # mostramos la foto en una etiqueta
        fondo.place(relx=0, rely=0, anchor='nw')             # blit en la pantalla 

        volver_b = CTkButton(fondo, 
                         hover_color=hover_color, fg_color=fg_color, bg_color='#ffffff',
                         corner_radius=3,
                         text='Volver  al  menu', text_color='#ffffff', font=('TypoGraphica',14),
                         width=200, height=43.78, command=self.volver_al_menu)
        volver_b.place(relx=x, rely=y, anchor = 'nw')
    
    def volver_al_menu(self):
        self.master.deiconify() # mostramos master de nuevo (master representa el self de un nivel superior / UiMenu) 
        self.withdraw()         # ocultamos Descripción