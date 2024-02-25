import sys
import pygame as pg
from Pantalla import Pantalla
from Juego import Juego

class Game:
    def __init__(self, WIDTH, HEIGTH):
        pg.init()
        pg.display.set_caption('3T')
        self.pantalla = pg.display.set_mode((WIDTH, HEIGTH))
        self.clock = pg.time.Clock()
        
        self.juego = Juego()
        self.pantalla_actual = Pantalla(self.pantalla)

    def run(self, FPS):
        self.ejecutando = True
        while self.ejecutando:    
            self.juego.jugar()
            print('A')
            self.pantalla_actual.update()
            self.clock.tick(FPS)

ui = Game(1280, 720) # Pantalla     
ui.run(60)
