import pygame as pg
from Jugador import Jugador
import cte
import UI_db.DataBase as db
import numpy as np

class Tablero2:
    def __init__(self, pantalla, pantalla_trans):


        # Instancias iniciales
        self.jugador1 = Jugador('Jug1','J1', 0, cte.VERDE)
        self.jugador2 = Jugador('Jug2', 'J2', 0, cte.ROJO)


        # Numpy trata las cadenas de caracteres como matrices de caracteres Unicode.
        # https://stackoverflow.com/questions/55377213/numpy-taking-only-first-character-of-string

        self.tablero = np.array([[[[[[[str((j+1)+(i*3))] for v in range(3)] for u in range(3)] for j in range(3)] for i in range(3)] for t in range(3)] for k in range(3)], 
                                dtype=np.dtype('U2')) # Establecemos la longitud de datos hasta 2 (usaremos 'J1' y 'J2')

        # i → filas                 para acceder a un elemento → [u, v, k, t, i, j],
        # j → columnas              equivale a → [M_fila, M_columna, m_fila, m_columna, fila, columna]
        # k → m_fila
        # t → m_columna
        # u → M_fila
        # v → M_columna

        # str((j*1)+(i*9)+(t*3)+(k*27) + 1)     # matriz del 1 al 81
        # str((j+1)+(i*3))                      # matriz del 1 al 9, 9 veces

        # np.dtype('U'+str(max([len(self.jugador1.simbolo), len(self.jugador2.simbolo)])))) → longitud adaptada a cualquier simbolo

        # Atributos de instancia
        self.pantalla = pantalla 
        self.pantalla_trans = pantalla_trans

        self.actual = self.jugador1     # Define quién está jugando actualmente (el turno del jugador)
        self.jug_ini = self.jugador1    # Guarda solamente quién hizo el primer movimiento de la partida

        self.num_mov = 0                # de momento no lo hemos usado, pero es recomendable implementarlo
        self.movimiento = (-1,-1)       # guarda la restricción de movimiento (matriz_f, matriz_c) que hay que jugar
                                        # (-1, -1) indica que no hay restricción de movimiento
