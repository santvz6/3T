import pygame as pg
#from main import WIDTH

class Menu:
    def __init__(self, pantalla, pantalla_trans):
        self.fondo_menu = pg.image.load('T1/Imagenes/Menu_boceto.png')
        self.pantalla = pantalla
        self.pantalla_trans = pantalla_trans
        self.x = 0
    
    def menu(self):
        self.pantalla.blit(self.fondo_menu,(0,0))

    def FondoMovimiento(self, fondo):
        x_relativa = self.x % fondo.get_rect().width
        self.pantalla.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
        if x_relativa < 1280:
            self.pantalla.blit(fondo, (x_relativa, 0))

        self.x -= 1