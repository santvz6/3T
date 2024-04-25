import sys
import pygame as pg
from Pantalla import Pantalla
import cte
import UI_db.DataBase as db
from UI_db.ui_login import UiLogin
 
# En main tendremos el código principal guardado en la clase Game
# El método __init__ recogerá las instancias de clases e iniciará pg.init()
# El método run se encargará de establecer el reloj de pygame y de actualizar en cada iteración la pantalla

class Game:
    def __init__(self, WIDTH, HEIGTH):

        db.tablaExiste('USUARIOS')  # Creación Tabla Usuarios en la db
        db.set_inactivo()           # Por si no se cerró sesión correctamente

        self.juego_inicial = ''

        self.ui = UiLogin(self)
        self.ui.mainloop()

        pg.init() # iniciamos pygame
        pg.display.set_caption('3T')
        self.pantalla = pg.display.set_mode((WIDTH, HEIGTH))
        self.clock = pg.time.Clock()
        
        self.pantalla_trans = pg.Surface((WIDTH, HEIGTH), pg.SRCALPHA) # superficie que admite colores transparentes

        self.pantalla_actual = Pantalla(self) # Pantalla → controla que display mostrar
        self.ejecutando = True
      
    def run(self, FPS):
        while self.ejecutando:  
            self.pantalla_actual.update() # actualizamos la pantalla por cada iteración del bucle
            self.clock.tick(FPS) # 60 iteraciones por segundo

# Usaremos el tamaño HD de pantalla
WIDTH = 1280
HEIGTH = 720
game = Game(WIDTH, HEIGTH)   
game.run(60)