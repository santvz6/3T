import sys
import pygame as pg
from Pantalla import Pantalla
import cte

class Game:
    def __init__(self, WIDTH, HEIGTH):
        pg.init()
        pg.display.set_caption('3T')
        pg.display.set_icon(cte.menu_boceto)
        self.pantalla = pg.display.set_mode((WIDTH, HEIGTH))
        self.clock = pg.time.Clock()
        
        self.pantalla_trans = pg.Surface((WIDTH, HEIGTH), pg.SRCALPHA)
        self.pantalla_actual = Pantalla(self.pantalla, self.pantalla_trans)

    def run(self, FPS):
        self.ejecutando = True
        while self.ejecutando:  
            self.pantalla_actual.update()
            self.clock.tick(FPS)

WIDTH = 1280
HEIGTH = 720
ui = Game(WIDTH, HEIGTH)   
ui.run(60)