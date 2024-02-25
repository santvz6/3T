import pygame as pg
import sys
from Reglas import reglas

# Pantalla se encargará de establecer cada tipo de escenario y de
# seleccionar mediante update() que escenario cargar
class Pantalla:
    BLANCO = (255,255,255)
    ROJO = (255,0,0)
    def __init__(self, pantalla):
        self.cambio_pantalla = '1t'
        self.pantalla = pantalla
        self.reglas = reglas # instancia de settings1

    def mostrar_texto(self, texto, fuente, tamaño, color, posicion):
        # Crear un objeto de texto
        font = pg.font.Font(fuente, tamaño)
        text_surface = font.render(texto, True, color)

        # Obtener el rectángulo del texto y configurar la posición
        text_rect = text_surface.get_rect()
        text_rect.topleft = posicion

        # Dibujar el texto en la pantalla
        self.pantalla.blit(text_surface, text_rect)

    def tablero_pg(self):
        self.fondo_1t = pg.image.load('T1/Imagenes/1t.png')
        self.fuente_p1 = ('T1/Fuentes/P1.ttf')
        self.pantalla.blit(self.fondo_1t,(0,0))
        for y in range(3):
            for x in range(3):
                self.mostrar_texto('X',self.fuente_p1,30,Pantalla.ROJO,(560+82*x,260+80*y))

        


    def prueba(self):
        self.pantalla.fill((100,100,100))

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            
        if self.cambio_pantalla == '1t':
            self.tablero_pg() # Dibujo del fondo

        
        elif self.cambio_pantalla == 'p':
            self.prueba()

        pg.display.update()
