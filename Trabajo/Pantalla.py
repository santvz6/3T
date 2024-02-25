import pygame as pg
import sys
from T1_settings import Tablero1
import cte

# Pantalla se encargará de establecer cada tipo de escenario y de
# seleccionar mediante update() que escenario cargar

class Pantalla:
    def __init__(self, pantalla):

        # Atributos de instancia
        self.pantalla = pantalla 
        self.cambio_pantalla = '1t' # pantalla actual

        # Instancias
        self.t1_set = Tablero1(self.pantalla)

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if self.cambio_pantalla == '1t':
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  
                    if not self.t1_set.victoria_1t():                     
                        self.t1_set.actualizar_1t()
                    

        if self.cambio_pantalla == '1t':
            if not self.t1_set.victoria_1t():
                self.t1_set.dbujar_1t() # Dibujo del fondo
            
            else:
                self.cambio_pantalla = 'p'

        
        elif self.cambio_pantalla == 'p':
            self.pantalla.fill(cte.BLANCO)

        pg.display.update()
