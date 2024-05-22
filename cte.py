""" cte.py
En este fichero guardaremos todos los datos constantes usados en el trabajo. 
Normalmente trabajaremos con tuplas para guardar distintos colores
y con rutas para acceder a imagenes y fuentes de letras.
"""

BLANCO = (255,255,255)
NEGRO = (0,0,0)

ROJO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)

# Transparentes
NEGRO_T = (0, 0, 0, 100)
BLANCO_T = (255,255,255, 45)
BLANCO2_T = (255, 255, 255, 110)
BLANCO3_T = (255, 255, 255, 195)

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

# Paleta de colores T3
verde_t3 = (195,217,134)

# Paleta + Transparentes
marron_t3_T = (150, 75, 0, 255)
gris_t3_T = (54, 54, 54, 255)
verde_t3_T = (195,217,134, 100)

# Imágenes
import pygame as pg

fondo_1t = pg.image.load('./Imagenes/1T/1t.png')
seleccion_1t = pg.image.load('./Imagenes/1T/seleccion_1t.png')
seleccion2_1t = pg.image.load('./Imagenes/1T/seleccion2_1t.png')
fondo_2t = pg.image.load('./Imagenes/2T/2t.png')
fondo_3t = pg.image.load('./Imagenes/3T/3t.png')
fondo_m35 = pg.image.load('./Imagenes/M35/M35.png')
easter_player = pg.image.load('./Imagenes/EG/eg.jpg')
easter_fondo = pg.image.load('./Imagenes/EG/fondo.png')

partida_default = ('./Imagenes/Partidas/Default.png')

# Fuentes de letra
fuente_p1 = ('./Fuentes/Principal.ttf')

import customtkinter as ctk
ctk.FontManager.load_font('./Fuentes/Principal.ttf')

import re
def transicion(string:str):
    # Patrón de la expresión regular
    patron = r'transicion(.*)'
    match = re.search(patron, string)
    if match:
        return ('transicion', match.group(1)) # devolvemos el segundo grupo de coincidencia → (.*)