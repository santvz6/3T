import pygame as pg
import numpy as np

# Ficheros
import cte

# Para ejecutar código desde main
from Settings.Jugador import Jugador

class Tablero3:
    def __init__(self, pantalla, pantalla_trans):

        #prueba
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
        self.movimiento = (-1,-1,-1,-1) # guarda la restricción de movimiento (m_fila, m_columna) que hay que jugar
                                        # (-1,-1,-1,-1) indica que no hay restricción de movimiento
        self.mini_victorias_1T = []
        self.mini_victorias_2T = []
    ########################### LÓGICA DE TURNOS ###########################
    # Mismo sistema que en 2T
    def turno(self):
        self.actual = self.jugador1 if self.jugador2 == self.actual else self.jugador2

    def jug_inicial(self):
        # Sirve para alternar quién comienza en cada nueva partida
        self.jug_ini = self.jugador1 if self.jugador2 == self.jug_ini else self.jugador2

    ########################### DIBUJO DEL TABLERO DE 3T ###########################

    # SÓLAMENTE se llama a la función cuando se realice un cambio sobre el tablero
    # de esta forma ahorramos recursos y optimizamos nuestro juego
    def dibujar_3t(self):
        self.pantalla.blit(cte.fondo_3t,(0,0))
        
        for M_fila in range(3):
            for M_columna in range(3):
                for m_fila in range(3):
                    for m_columna in range(3):
                        for fila in range(3):
                            for columna in range(3):
                                x = 282 + 242 * M_columna + 82 * m_columna + 80 / 3 * columna  # la 'x' se mueve por columnas
                                y = -3 + 240 * M_fila + 80 * m_fila + 80 / 3 * fila  # la 'y' se mueve por filas
                                match self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna]:
                                    case self.jugador1.simbolo:
                                        color = (255, 0, 0, 100)
                                    case self.jugador2.simbolo:
                                        color = (0, 0, 255, 100)
                                    case _:
                                        color = cte.BLANCO2_T
                                self.mostrar_texto(self.pantalla_trans, self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna],  cte.fuente_p1, 26, color, (x, y))



    # Propósito: SÓLO para iluminar por dónde se desliza el cursor
    # Está ejecutandose constantemente (tiene un único propósito para no ocasionar lag)
    def dibujar_3t_on(self):
            m_pos = pg.mouse.get_pos()                                                             
            self.pantalla.blit(cte.fondo_3t,(0,0))

            if 280 < m_pos[0] < 1000  and 0 < m_pos[1] < 720:                 
                for M_fila in range(3):
                    for M_columna in range(3):
                        for m_fila in range(3):
                            for m_columna in range(3):
                                for fila in range(3):
                                    for columna in range(3):
                                        x = 282 + 242*M_columna + 82*m_columna + 80/3*columna   # la 'x' se mueve por columnas
                                        y = -3 + 240*M_fila + 80*m_fila + 80/3*fila
                                         
                                        if x < m_pos[0] < x+80/3  and y < m_pos[1] < y+80/3:  
                                                      # la 'y' se mueve por filas

                                            self.mostrar_texto(self.pantalla,self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna],cte.fuente_p1,26,cte.BLANCO,(x, y))


    ########################### REGISTRO DE JUGADAS REALIZADAS Y PRÓXIMAS JUGADAS ###########################

    def definir_restriccion(self, M_fila:int, M_columna:int, m_fila:int, m_columna:int):
        # Se establece la restriccion si el movimiento anterior no esta en un tablero ganado

        if (M_fila, M_columna) not in self.mini_victorias_2T:
            if (M_fila, M_columna, m_fila, m_columna) not in self.mini_victorias_1T:
                self.movimiento = (M_fila, M_columna, m_fila, m_columna)
                self.turno()

            else:
                self.movimiento = (M_fila, M_columna, -1, -1)
                self.turno()
        # Si se trata de un tablero ganado = movimiento libre
        else:
            self.movimiento = (-1, -1, -1, -1)
            self.turno()

    # Actualizacion del tablero al hacer click

    def actualizar_3t_mouse(self):
        # Usamos teclas

        # Usamos el mouse
        m_pos = pg.mouse.get_pos()  # obtenemos la posición del mouse cuando se hizo click
        for M_fila in range(3):
            for M_columna in range(3):
                for m_fila in range(3):
                    for m_columna in range(3):
                        for fila in range(3):
                            for columna in range(3):

                                # Las coordenadas dependen de la matriz_f y matriz_c
                                if self.movimiento == (-1, -1, -1, -1):
                                    x = 280 + 242 * M_columna + 82 * m_columna + 80 / 3 * columna  # la 'x' se mueve por columnas
                                    y = 0 + 240 * M_fila + 80 * m_fila + 80 / 3 * fila  # la 'y' se mueve por filas

                                elif self.movimiento == (M_fila, M_columna, -1, -1):
                                    x = 280 + 242 * self.movimiento[1] + 82 * m_columna + 80 / 3 * columna  # la 'x' se mueve por columnas
                                    y = 0 + 240 * self.movimiento[0] + 80 * m_fila + 80 / 3 * fila  # la 'y' se mueve por filas

                                else:
                                    x = 280 + 242 * self.movimiento[1] + 82 * self.movimiento[3] + 80 / 3 * columna  # la 'x' se mueve por columnas
                                    y = 0 + 240 * self.movimiento[0] + 80 * self.movimiento[2] + 80 / 3 * fila  # la 'y' se mueve por filas

                                # Calculamos la posición de cada número
                                if x < m_pos[0] < x + 80 / 3 and y < m_pos[1] < y + 80 / 3:
                                    # Solo si el tablero a jugar es valido
                                    if (M_fila, M_columna) not in self.mini_victorias_2T:
                                        if (M_fila, M_columna, m_fila, m_columna) not in self.mini_victorias_1T:

                                            # Movimiento libre
                                            if self.movimiento == (-1, -1, -1, -1):

                                                if self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna] in [str(_ + 1) for _ in range(9)]:
                                                    self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna] = self.actual.simbolo
                                                    self.mini_victorias_1T = self.get_mini_victorias_1T()
                                                    self.mini_victorias_2T = self.get_mini_victorias_2T(self.mini_victorias_1T)
                                                    self.definir_restriccion(m_fila, m_columna, fila, columna)
                                                    self.num_mov += 1

                                            # Movimiento con semirestriccion
                                            elif self.movimiento == (M_fila, M_columna, -1, -1):

                                                if self.tablero[self.movimiento[0], self.movimiento[1], m_fila, m_columna, fila, columna] in [str(_ + 1) for _ in range(9)]:
                                                    self.tablero[self.movimiento[0], self.movimiento[1], m_fila, m_columna, fila, columna] = self.actual.simbolo
                                                    self.mini_victorias_1T = self.get_mini_victorias_1T()
                                                    self.mini_victorias_2T = self.get_mini_victorias_2T(self.mini_victorias_1T)
                                                    self.definir_restriccion(m_fila, m_columna, fila, columna)
                                                    self.num_mov += 1

                                            # Movimiento completamente restringido
                                            else:

                                                 if self.tablero[self.movimiento[0], self.movimiento[1], self.movimiento[2], self.movimiento[3], fila, columna] in [str(_ + 1) for _ in range(9)]:
                                                    self.tablero[self.movimiento[0], self.movimiento[1], self.movimiento[2], self.movimiento[3], fila, columna] = self.actual.simbolo
                                                    self.mini_victorias_1T = self.get_mini_victorias_1T()
                                                    self.mini_victorias_2T = self.get_mini_victorias_2T(self.mini_victorias_1T)
                                                    self.definir_restriccion(self.movimiento[2], self.movimiento[3], fila, columna)
                                                    self.num_mov += 1



    ########################### EJECUCIÓN DE T3 ###########################
    def update(self):
        self.dibujar_3t_on()
        self.pantalla.blit(self.pantalla_trans,(0,0))





    ########################### CONDICIONES DE VICTORIA #################################
    # Matriz tamaño 1T ganada
    def matriz_ganada_1T(self, M_fila:int, M_columna:int, m_fila:int, m_columna:int, ganador:str):
        for fila_1T in range(3):
            for columna_1T in range(3):
                self.tablero[M_fila, M_columna, m_fila, m_columna, fila_1T, columna_1T] = ganador
    # Matriz tamaño 2T ganada, actualmente rellena todas las matrices 3 x 3 dentro del 2T con el simbolo ganador
    def matriz_ganada_2T(self, M_fila:int, M_columna:int, ganador:str):
        for fila_2T in range(3):
            for columna_2T in range(3):
                self.matriz_ganada_1T(M_fila, M_columna, fila_2T, columna_2T, ganador)
    # Estudia si alguna matriz 3 x 3 se ha ganado
    def get_mini_victorias_1T(self):
        mini_victorias_1T = []

        # Iteramos todas las matrices 3 x 3 del tablero
        for M_fila in range(3):
            for M_columna in range(3):
                for m_fila in range(3):
                    for m_columna in range(3):

                        # Verificar filas
                        for fila in self.tablero[M_fila, M_columna, m_fila, m_columna]:
                            if fila[0] == fila[1] == fila[2]:
                                self.matriz_ganada_1T(M_fila, M_columna, m_fila, m_columna, fila[0])
                                mini_victorias_1T.append((M_fila, M_columna, m_fila, m_columna)) # Tupla de matriz de coordenadas 3 x 3 ganada
                        # Verificar columnas
                        for columna in range(3):
                            if self.tablero[M_fila, M_columna, m_fila, m_columna, 0, columna] == self.tablero[M_fila, M_columna, m_fila, m_columna, 1, columna] == self.tablero[M_fila, M_columna, m_fila, m_columna, 2, columna]:
                                self.matriz_ganada_1T(M_fila, M_columna, m_fila, m_columna, self.tablero[M_fila, M_columna, m_fila, m_columna, 0, columna])
                                mini_victorias_1T.append((M_fila, M_columna, m_fila, m_columna))
                        # Verificar diagonales
                        if self.tablero[M_fila, M_columna, m_fila, m_columna, 0, 0] == self.tablero[M_fila, M_columna, m_fila, m_columna, 1, 1] == \
                                self.tablero[M_fila, M_columna, m_fila, m_columna, 2, 2]:
                            self.matriz_ganada_1T(M_fila, M_columna, m_fila, m_columna, self.tablero[M_fila, M_columna, m_fila, m_columna, 0, 0])
                            mini_victorias_1T.append((M_fila, M_columna, m_fila, m_columna))

                        if self.tablero[M_fila, M_columna, m_fila, m_columna, 0, 2] == self.tablero[M_fila, M_columna, m_fila, m_columna, 1, 1] == \
                                self.tablero[M_fila, M_columna, m_fila, m_columna, 2, 0]:
                            self.matriz_ganada_1T(M_fila, M_columna, m_fila, m_columna, self.tablero[M_fila, M_columna, m_fila, m_columna, 0, 2])
                            mini_victorias_1T.append((M_fila, M_columna, m_fila, m_columna))
        return mini_victorias_1T

    # Estudia si alguna matriz del 2T se ha ganado
    def get_mini_victorias_2T(self, mini_victorias_1T:list):
        mini_victorias_2T = []

        # Iteramos todas las matrices 2T del tablero
        for M_fila in range(3):
            for M_columna in range(3):
                # Itero en la lista de matrices 3x3 ganadas
                victorias_M = []
                for victoria_1T in mini_victorias_1T:
                    if M_fila == victoria_1T[0] and M_columna == victoria_1T[1]:
                        victorias_M.append((victoria_1T[2], victoria_1T[3]))

                # Verifico filas
                for fila in range(3):
                    if (fila,0) in victorias_M and (fila,1) in victorias_M and (fila,2) in victorias_M:
                        self.matriz_ganada_2T(M_fila, M_columna, self.tablero[M_fila, M_columna, fila , 0, 0, 0])
                        mini_victorias_2T.append((M_fila, M_columna))

                # Verifico columnas
                for columna in range(3):
                        if (0, columna) in victorias_M and (1, columna) in victorias_M and (2, columna) in victorias_M:
                            self.matriz_ganada_2T(M_fila, M_columna, self.tablero[M_fila, M_columna, 0, columna, 0, 0])
                            mini_victorias_2T.append((M_fila, M_columna))

                # Verifico diagonales
                if (0, 0) in victorias_M and (1, 1) in victorias_M and (2, 2) in victorias_M:
                    self.matriz_ganada_2T(M_fila, M_columna, self.tablero[M_fila, M_columna, 0, 0, 0, 0])
                    mini_victorias_2T.append((M_fila, M_columna))
                elif (0, 2) in victorias_M and (1, 1) in victorias_M and (2, 0) in victorias_M:
                    self.matriz_ganada_2T(M_fila, M_columna, self.tablero[M_fila, M_columna, 0, 2, 0, 0])
                    mini_victorias_2T.append((M_fila, M_columna))
        return mini_victorias_2T

    # Condición de victoria total
    def victoria_3t(self):

        # Transformamos mini_victorias en un array de 3x3
        victoria_array = np.array([[a * 3 + b for b in range(3)] for a in range(3)], dtype=np.dtype('U2'))

        for (fila, columna) in self.mini_victorias_2T:
            victoria_array[fila, columna] = self.tablero[fila, columna, 0, 0]

        # Verificar filas
        for fila in victoria_array:
            if fila[0] == fila[1] == fila[2]:
                return True, fila[0]

        # Verificar columnas
        for columna in range(3):
            if victoria_array[0, columna] == victoria_array[1, columna] == victoria_array[2, columna]:
                return (True, victoria_array[0, columna])

                # Verificar diagonales
        if victoria_array[0, 0] == victoria_array[1, 1] == victoria_array[2, 2]:
            return (True, victoria_array[0, 0])

        if victoria_array[0, 2] == victoria_array[1, 1] == victoria_array[2, 0]:
            return (True, victoria_array[0, 2])

        return (False, None)


############################ REINICIO DE 3T ##############################
    def reinicio_3t(self):
        self.tablero = np.array([[[[[[str((v+1)+(u*3)) for v in range(3)] for u in range(3)] for j in range(3)] for i in range(3)] for t in range(3)] for k in range(3)],
                                dtype=np.dtype('U2'))
        self.num_mov = 0            # reiniciamos el número de movimientos
        self.jug_inicial()          # cambiamos quién empieza en la nueva ronda
        self.actual = self.jug_ini  # y lo registramos
        self.movimiento = (-1, -1)  # el primer movimiento no tiene restricciones


########################### BOTONES DURANTE EL JUEGO ####################


########################### TEXTO #######################################
    def mostrar_texto(self, pantalla_int, texto: str, fuente, tamaño: int, color: tuple | str, posicion: tuple):
        # Crear un objeto de texto
        font = pg.font.Font(fuente, tamaño)
        text_surface = font.render(texto, True, color)

        # Obtener el rectángulo del texto y configurar la posición
        text_rect = text_surface.get_rect()
        text_rect.topleft = posicion

        # Dibujar el texto en la pantalla
        if pantalla_int == self.pantalla_trans:
            text_surface.set_alpha(color[3])  # render elimina la opacidad
            self.pantalla_trans.blit(text_surface, text_rect)

        elif pantalla_int == self.pantalla:
            self.pantalla.blit(text_surface, text_rect)
