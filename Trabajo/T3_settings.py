import pygame as pg
from Jugador import Jugador
import cte
import UI_db.DataBase as db
import numpy as np

class Tablero3:
    def __init__(self, pantalla, pantalla_trans):


        # Instancias iniciales
        self.jugador1 = Jugador('Jug1','J1', 0, cte.VERDE)
        self.jugador2 = Jugador('Jug2', 'J2', 0, cte.ROJO)


        # Numpy trata las cadenas de caracteres como matrices de caracteres Unicode.
        # https://stackoverflow.com/questions/55377213/numpy-taking-only-first-character-of-string

        self.tablero = np.array([[[[[[str((v+1)+(u*3)) for v in range(3)] for u in range(3)] for j in range(3)] for i in range(3)] for t in range(3)] for k in range(3)], 
                                dtype=np.dtype('U2')) # Establecemos la longitud de datos hasta 2 (usaremos 'J1' y 'J2')

        # i → filas                 para acceder a un elemento → [u, v, k, t, i, j],
        # j → columnas              equivale a → [M_fila, M_columna, m_fila, m_columna, fila, columna]
        # k → m_fila
        # t → m_columna
        # u → M_fila
        # v → M_columna

        # str((j+1)+(i*3))                      # matriz del 1 al 9, 9 veces

        # np.dtype('U'+str(max([len(self.jugador1.simbolo), len(self.jugador2.simbolo)])))) → longitud adaptada a cualquier simbolo

        # Atributos de instancia
        self.pantalla = pantalla 
        self.pantalla_trans = pantalla_trans

        self.actual = self.jugador1     # Define quién está jugando actualmente (el turno del jugador)
        self.jug_ini = self.jugador1    # Guarda solamente quién hizo el primer movimiento de la partida

        self.num_mov = 0                # de momento no lo hemos usado, pero es recomendable implementarlo
        self.movimiento = (-1,-1)       # guarda la restricción de movimiento (m_fila, m_columna) que hay que jugar
                                        # (-1, -1) indica que no hay restricción de movimiento
        
        
    # SÓLAMENTE se llama a la función cuando se realice un cambio sobre el tablero
    # de esta forma ahorramos recursos y optimizamos nuestro juego
    def dibujar_3t(self, m_victorias: list, M_victorias: list):
        self.pantalla.blit(cte.fondo_3t,(0,0))
        
        for M_fila in range(3):
            for M_columna in range(3):
                for m_fila in range(3):
                    for m_columna in range(3):
                        for fila in range(3):
                            for columna in range(3):

                                x = 280 + 242*M_columna + 82*m_columna + 80/3*columna    # la 'x' se mueve por columnas
                                y = 0 + 240*M_fila + 80*m_fila + 80/3*fila               # la 'y' se mueve por filas

                                #  m_victorias
                                if (M_fila, M_columna, m_fila, m_columna) in m_victorias:
                                    if self.tablero[M_fila, M_columna, m_fila, m_columna, 0, 0] == self.jugador1.simbolo:
                                        self.mostrar_texto(self.pantalla,self.jugador1.simbolo,cte.fuente_p1,80,self.jugador1.color,
                                                        (390 + 200*m_columna,115 + 190*m_fila))
                                    else:
                                        self.mostrar_texto(self.pantalla,self.jugador2.simbolo,cte.fuente_p1,80,self.jugador2.color,
                                                        (390 + 200*m_columna,115 + 190*m_fila))
                                # M_victorias
                                if (M_fila, M_columna) in M_victorias:
                                    if self.tablero[M_fila, M_columna, 0, 0, 0, 0] == self.jugador1.simbolo:
                                        self.mostrar_texto(self.pantalla,self.jugador1.simbolo,cte.fuente_p1,80,self.jugador1.color,
                                                        (390 + 200*m_columna,115 + 190*m_fila))
                                    else:
                                        self.mostrar_texto(self.pantalla,self.jugador2.simbolo,cte.fuente_p1,80,self.jugador2.color,
                                                        (390 + 200*m_columna,115 + 190*m_fila))



                                # Dibujar matriz sin minivictoria
                                else:
                                    if self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna] == self.jugador1.simbolo:
                                        self.mostrar_texto(self.pantalla,self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna],cte.fuente_p1,26,self.jugador1.color,(x, y))

                                    elif self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna] == self.jugador2.simbolo:
                                        self.mostrar_texto(self.pantalla,self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna],cte.fuente_p1,26,self.jugador2.color,(x, y))

                                    # Casillas no jugadas
                                    else:
                                        if m_fila == self.movimiento[0] and m_columna == self.movimiento[1]:
                                            self.mostrar_texto(self.pantalla_trans,self.tablero[self.movimiento[0], self.movimiento[1], fila, columna],cte.fuente_p1,26,cte.BLANCO2_T,(x, y))
                                        # Incluye self.movimiento (-1, -1 → nunca coincide)
                                        else:
                                            self.mostrar_texto(self.pantalla_trans,self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna],cte.fuente_p1,26,cte.BLANCO_T,(x, y))                                    



    # Propósito: SÓLO para iluminar por dónde se desliza el cursor
    # Está ejecutandose constantemente (tiene un único propósito para no ocasionar lag)
    def dibujar_3t_on(self, mini_victorias:list):
            m_pos = pg.mouse.get_pos()                                                             
            self.pantalla.blit(cte.fondo_3t,(0,0))

            if 280 < m_pos[0] < 1000  and 0 < m_pos[1] < 720:                 
                for M_fila in range(3):
                    for M_columna in range(3):
                        for m_fila in range(3):
                            for m_columna in range(3):
                                for fila in range(3):
                                    for columna in range(3):
                                        x = 280 + 242*M_columna + 82*m_columna + 80/3*columna   # la 'x' se mueve por columnas
                                        y = 0 + 240*M_fila + 80*m_fila + 80/3*fila   
                                         
                                        if x < m_pos[0] < x+80/3  and y < m_pos[1] < y+80/3:  
                                                      # la 'y' se mueve por filas

                                            self.mostrar_texto(self.pantalla,self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna],cte.fuente_p1,26,cte.BLANCO,(x, y))
                                                            

    def update(self):
        self.dibujar_3t_on([])
        self.pantalla.blit(self.pantalla_trans,(0,0))



########################### TEXTO ###########################
    def mostrar_texto(self, pantalla_int, texto:str, fuente, tamaño:int, color:tuple|str, posicion:tuple):
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
