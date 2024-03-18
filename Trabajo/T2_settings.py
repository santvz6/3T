import pygame as pg
from Jugador import Jugador
import cte
import UI_db.DataBase as db
import numpy as np

class Tablero2:
    def __init__(self, pantalla, pantalla_trans):

        # Creación del tablero
        # i → filas, j → columnas, k → matriz_filas, t → matriz_columnas
 
        self.tablero = np.array([[[[str((i+1)+(j*3)) for j in range(3)] for i in range(3)] for t in range(3)] for k in range(3)])
        # 360 + 200*matriz_f+fila*200/3, 70 + 200*matriz_c+columna*200/3
        # str((i*1)+(j*9)+(k*3)+(t*27) + 1)


        #print(self.tablero)

        # Instancias iniciales
        self.jugador1 = Jugador('Jug1','J1', 0, cte.amarillo_t1)
        self.jugador2 = Jugador('Jug2', 'J2', 0, cte.azul_1)

        # Atributos de instancia
        self.pantalla = pantalla 
        self.pantalla_trans = pantalla_trans
        self.actual = self.jugador1 # Primer movimiento
        self.jug_ini = self.jugador1 # Cambio de

        self.transparencia = 255
        self.num_mov = 0





    def mostrar_texto(self,pantalla_int, texto, fuente, tamaño, color, posicion):
        # Crear un objeto de texto
        font = pg.font.Font(fuente, tamaño)
        text_surface = font.render(texto, True, color)
        
        # Obtener el rectángulo del texto y configurar la posición
        text_rect = text_surface.get_rect()
        text_rect.topleft = posicion

        # Dibujar el texto en la pantalla
        if pantalla_int == self.pantalla_trans:
            text_surface.set_alpha(color[3]) # render elimina la opacidad
            self.pantalla_trans.blit(text_surface, text_rect)

        elif pantalla_int == self.pantalla:
            self.pantalla.blit(text_surface, text_rect)




    def dibujar(self):
        print('DIMENSIONES: ', self.tablero.shape)
        self.pantalla.blit(cte.fondo_2t,(0,0))
        #self.pantalla.fill(cte.NEGRO)
        for matriz_f in range(3):
            for matriz_c in range(3):
                for fila in range(3):
                    for columna in range(3):
                        print(self.tablero[matriz_f, matriz_c, fila, columna])
                        if self.tablero[matriz_f, matriz_c, fila, columna] == self.jugador1.simbolo:
                            self.mostrar_texto(self.pantalla,self.tablero[matriz_f, matriz_c, fila, columna],cte.fuente_p1,35,self.jugador1.color,(200*matriz_f+fila*200/3, 200*matriz_c+columna*200/3))
                                            
                        elif self.tablero[matriz_f, matriz_c, fila, columna] == self.jugador2.simbolo:
                            self.mostrar_texto(self.pantalla,self.tablero[matriz_f, matriz_c, fila, columna],cte.fuente_p1,35,self.jugador2.color,(200*matriz_f+fila*200/3, 200*matriz_c+columna*200/3))

                        else:
                            self.mostrar_texto(self.pantalla,self.tablero[matriz_f, matriz_c, fila, columna],cte.fuente_p1,35,cte.BLANCO,(360 + 200*matriz_f+fila*200/3, 110 + 200*matriz_c+columna*200/3))
      
   


    