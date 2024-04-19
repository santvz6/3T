BLANCO = (255,255,255)
NEGRO = (0,0,0)

ROJO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)

# Transparentes
NEGRO_T = (0, 0, 0, 100)
BLANCO_T = (255,255,255, 60)
BLANCO2_T = (255, 255, 255, 150)

# Paleta de colores T1
amarillo_t1 = (248, 211, 32)
azul_1 = (0, 153, 255)

# Paleta + Transparentes
amarillo_t1_T = (248, 211, 32,100)
amarillo_t1_T2 = (248, 211, 32,160)

# Paleta de colores T2
amarillo_t2 = (255,215,0)
gris_t2 = (54,54,54)
naranja_t2 = (198, 101, 51)

# Paleta + Transparentes
naranja_t2_T = (198, 101, 51, 100)


# Imágenes
import pygame as pg

fondo_1t = pg.image.load('./Imagenes/1T/1t.png')
fondo_2t = pg.image.load('./Imagenes/2T/2t.png')

# Fuentes de letra
fuente_p1 = ('./Fuentes/P1.ttf')

import customtkinter as ctk
ctk.FontManager.load_font('./Fuentes/P1.ttf')