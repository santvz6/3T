from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
from tkinter import font

app = CTk() #https://customtkinter.tomschimansky.com/documentation/widgets/label
app.geometry("1280x720")
app.resizable(0,0)

#set_default_color_theme('green')
#set_appearance_mode('light')


lateral = CTkFrame(master=app, fg_color="#7C188E",  width=280, height=720, corner_radius=0)
lateral.pack_propagate(0) # desactivamos la propagación de tamaño si se añaden widgets
lateral.pack(fill="y", anchor="w", side="left")

label = CTkLabel(master=lateral, text='The Terrorist\nTeam', font=('TypoGraphica', 40), 
                 fg_color='transparent', text_color='#FFFFFF')
label.place(relx=0.5, rely=0.2, anchor='center')

label2 = CTkLabel(master=lateral, text='Santiago Alvarez\nPau Mateo\nDavid Martinez\nCarlos Vidal\nAlex Garre', font=('TypoGraphica', 17), 
                  fg_color='transparent', text_color='#FFFFFF',justify='left')
label2.place(relx=0.32, rely=0.9, anchor='center')


### --- Carga de Minijuegos --- ### 

# Cargamos Imagenees
t1 = CTkImage(light_image=Image.open('T1/Imagenes/1t.png'), dark_image=Image.open('T1/Imagenes/1t.png'), size=(100,100))
t2 = CTkImage(light_image=Image.open('T1/Imagenes/1t.png'), dark_image=Image.open('T1/Imagenes/1t.png'), size=(100,100))
t3 = CTkImage(light_image=Image.open('T1/Imagenes/1t.png'), dark_image=Image.open('T1/Imagenes/1t.png'), size=(100,100))
mj = CTkImage(light_image=Image.open('T1/Imagenes/1t.png'), dark_image=Image.open('T1/Imagenes/1t.png'), size=(100,100))

t1_labbel = CTkLabel(app, image=t1, text="") 
t1_labbel.place(relx=0.37, rely=0.08, anchor='nw') # anchor = nortwest
t2_labbel = CTkLabel(app, image=t1, text="") 
t2_labbel.place(relx=0.37, rely=0.31, anchor='nw')
t3_labbel = CTkLabel(app, image=t1, text="")  
t3_labbel.place(relx=0.37, rely=0.53, anchor='nw')
mj_labbel = CTkLabel(app, image=t1, text="")  
mj_labbel.place(relx=0.37, rely=0.75, anchor='nw')



#families = font.families()
# Imprimir la lista de familias de fuentes
#print(families)

app.mainloop()
