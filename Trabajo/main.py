import sys
import pygame as pg
from Pantalla import Pantalla
import cte
import UI_db.DataBase as db
from UI_db.ui_login import UiLogin



class Game:
    def __init__(self, WIDTH, HEIGTH):

        db.tablaExiste('USUARIOS') # Creación Tabla Usuarios en la db
        db.set_inactivo()

        self.juego_inicial = ''

        self.ui = UiLogin(self)
        self.ui.mainloop()

        pg.init() # iniciamos pygame
        pg.display.set_caption('3T')
        self.pantalla = pg.display.set_mode((WIDTH, HEIGTH))
        self.clock = pg.time.Clock()
        
        self.pantalla_trans = pg.Surface((WIDTH, HEIGTH), pg.SRCALPHA) # superficie que admite colores transparentes
        self.pantalla_actual = Pantalla(self.pantalla, self.pantalla_trans, self.juego_inicial, self) # Pantalla controla que display mostrar

        self.ejecutando = True
      
    def run(self, FPS):
        while self.ejecutando:  
            self.pantalla_actual.update() # actualizamos la pantalla por cada iteración del bucle
            self.clock.tick(FPS) # 60 iteraciones por segundo


WIDTH = 1280
HEIGTH = 720
ui = Game(WIDTH, HEIGTH)   
ui.run(60)
