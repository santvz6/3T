import pygame as pg
import numpy as np

# Ficheros
import cte

# Para ejecutar código desde main
from Settings.Jugador import Jugador

class Tablero3:
    def __init__(self, pantalla, pantalla_trans):

        # Instancias iniciales
        self.jugador1 = Jugador('Jug1','J1', 0, cte.marron_t3_T)
        self.jugador2 = Jugador('Jug2', 'J2', 0, cte.gris_t3_T)


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
        self.jugador_inicial = self.jugador1    # Guarda solamente quién hizo el primer movimiento de la partida

        self.num_mov = 0                # de momento no lo hemos usado, pero es recomendable implementarlo
        self.restriccion = (-1,-1,-1,-1) # guarda la restricción de movimiento (m_fila, m_columna) que hay que jugar
                                        # (-1,-1,-1,-1) indica que no hay restricción de movimiento
        self.mini_victorias_1T = []
        self.mini_victorias_2T = []

        """
        ganar:      Victoria total
        ganar_2t:   Completar matriz 2T
        ganar_1t:   Completar matriz 1T
        """
        self.probar_3t(condicion='')
        self.dibujar_3t()
        

        
###                   REGLAS Y CONFIGURACIONES DEL JUEGO                  ###

    def cambiar_turno(self):
        """
        Cambia el turno entre los jugadores.
        """
        self.actual = self.jugador1 if self.jugador2 == self.actual else self.jugador2

    def cambiar_juginicial(self):
        """
        Alterna quién comienza en cada nueva partida.
        """
        self.jugador_inicial = self.jugador1 if self.jugador2 == self.jugador_inicial else self.jugador2

    def definir_restriccion(self, M_fila:int, M_columna:int, m_fila:int, m_columna:int):
        """
        Establece la restricción de movimiento para el rival

        Parámetros
        ---------
        m_fila: int
            Representa la fila jugada, se transforma en m_fila
        m_columna: int
            Representa la columna jugada, se transforma en m_columna
        """ 

        if (M_fila, M_columna) not in self.mini_victorias_2T:
            if (M_fila, M_columna, m_fila, m_columna) not in self.mini_victorias_1T:
                self.restriccion = (M_fila, M_columna, m_fila, m_columna)
                self.cambiar_turno()

            else:
                self.restriccion = (M_fila, M_columna, -1, -1)
                self.cambiar_turno()
        # Si se trata de un tablero ganado = movimiento libre
        else:
            self.restriccion = (-1, -1, -1, -1)
            self.cambiar_turno()

    def probar_3t(self, condicion=''):
        for M_fila in range(3):
            for M_columna in range(3):
                for m_fila in range(3):
                    for m_columna in range(3):
                        for fila in range(3):
                            for columna in range(3):
                                match condicion:
                                    case 'ganar':
                                        if M_fila==0 and (M_columna!=2 or M_columna==2 and m_fila==0 and fila==0 and columna!=2):
                                            self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna] = self.jugador1.simbolo
                                    case 'ganar_2t':
                                        if fila == 0 and m_fila==0 and (m_columna!=2 or m_columna==2 and columna!=2):
                                            self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna] = self.jugador1.simbolo
                                    case 'ganar_1t':
                                        if fila==0 and columna!=2:
                                            self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna] = self.jugador1.simbolo
                                    case _:
                                        pass

                                    
###                   COMPROBACIONES Y ACTUALIZACIONES               ###

    def jugar_casilla(self, unicode:int|bool):
        """
        Actualiza la casilla del tablero según la jugada realizada por el usuario.

        Parámetros
        ----------
        unicode : bool|int
            Si es un entero, representa la casilla de la tecla presionada. Si es False, se usa la posición del mouse para determinar la casilla.
        """

        if unicode:
            pass
        else:
            m_pos = pg.mouse.get_pos()  # obtenemos la posición del mouse cuando se hizo click
            for M_fila in range(3):
                for M_columna in range(3):
                    for m_fila in range(3):
                        for m_columna in range(3):
                            for fila in range(3):
                                for columna in range(3):

                                    # Las coordenadas dependen de la matriz_f y matriz_c
                                    if self.restriccion == (-1, -1, -1, -1):
                                        x = 280 + 242 * M_columna + 82 * m_columna + 80 / 3 * columna  # la 'x' se mueve por columnas
                                        y = 0 + 240 * M_fila + 80 * m_fila + 80 / 3 * fila  # la 'y' se mueve por filas

                                    elif self.restriccion == (M_fila, M_columna, -1, -1):
                                        x = 280 + 242 * self.restriccion[1] + 82 * m_columna + 80 / 3 * columna  # la 'x' se mueve por columnas
                                        y = 0 + 240 * self.restriccion[0] + 80 * m_fila + 80 / 3 * fila  # la 'y' se mueve por filas

                                    else:
                                        x = 280 + 242 * self.restriccion[1] + 82 * self.restriccion[3] + 80 / 3 * columna  # la 'x' se mueve por columnas
                                        y = 0 + 240 * self.restriccion[0] + 80 * self.restriccion[2] + 80 / 3 * fila  # la 'y' se mueve por filas

                                    # Calculamos la posición de cada número
                                    if x < m_pos[0] < x + 80 / 3 and y < m_pos[1] < y + 80 / 3:
                                        # Solo si el tablero a jugar es valido
                                        if (M_fila, M_columna) not in self.mini_victorias_2T:
                                            if (M_fila, M_columna, m_fila, m_columna) not in self.mini_victorias_1T:

                                                # Movimiento libre
                                                if self.restriccion == (-1, -1, -1, -1):

                                                    if self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna] in [str(_ + 1) for _ in range(9)]:
                                                        self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna] = self.actual.simbolo
                                                        self.mini_victorias_1T = self.get_mini_victorias_1T()
                                                        self.mini_victorias_2T = self.get_mini_victorias_2T(self.mini_victorias_1T)
                                                        self.definir_restriccion(m_fila, m_columna, fila, columna)
                                                        self.num_mov += 1

                                                # Movimiento con semirestriccion
                                                elif self.restriccion == (M_fila, M_columna, -1, -1):

                                                    if self.tablero[self.restriccion[0], self.restriccion[1], m_fila, m_columna, fila, columna] in [str(_ + 1) for _ in range(9)]:
                                                        self.tablero[self.restriccion[0], self.restriccion[1], m_fila, m_columna, fila, columna] = self.actual.simbolo
                                                        self.mini_victorias_1T = self.get_mini_victorias_1T()
                                                        self.mini_victorias_2T = self.get_mini_victorias_2T(self.mini_victorias_1T)
                                                        self.definir_restriccion(m_fila, m_columna, fila, columna)
                                                        self.num_mov += 1

                                                # Movimiento completamente restringido
                                                else:

                                                    if self.tablero[self.restriccion[0], self.restriccion[1], self.restriccion[2], self.restriccion[3], fila, columna] in [str(_ + 1) for _ in range(9)]:
                                                        self.tablero[self.restriccion[0], self.restriccion[1], self.restriccion[2], self.restriccion[3], fila, columna] = self.actual.simbolo
                                                        self.mini_victorias_1T = self.get_mini_victorias_1T()
                                                        self.mini_victorias_2T = self.get_mini_victorias_2T(self.mini_victorias_1T)
                                                        self.definir_restriccion(self.restriccion[2], self.restriccion[3], fila, columna)
                                                        self.num_mov += 1

    def matriz_ganada_1T(self, M_fila:int, M_columna:int, m_fila:int, m_columna:int, ganador:str):
        for fila_1T in range(3):
            for columna_1T in range(3):
                self.tablero[M_fila, M_columna, m_fila, m_columna, fila_1T, columna_1T] = ganador

    def matriz_ganada_2T(self, M_fila:int, M_columna:int, ganador:str):
        """
        Rellenamos toda una matriz de 3x3 con el simbolo ganador

        Parámetros
        ----------
        M_fila: int
            Representa la fila de la matriz 2T
        M_columna: int
            Representa la columna de la matriz 2T
        ganador: str
            Representa el símbolo del jugador que ganó la matriz grande
        """        
                
        for fila_2T in range(3):
            for columna_2T in range(3):
                self.matriz_ganada_1T(M_fila, M_columna, fila_2T, columna_2T, ganador)

    # Estudia si alguna matriz 3 x 3 se ha ganado
    def get_mini_victorias_1T(self):
        """
        Se estará cuándo el jugador juegue alguna casilla.
        Registra condiciones de victoria dentro de cada matriz 3x3 ...
        """
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

    def victoria_3t(self):
        """
        Verifica si hay un ganador en el juego

        Devuelve
        --------
        tuple
            Devuelve una tupla con un valor booleano (indica si hay victoria)
            y el símbolo del ganador de la partida
        """
        # Transformamos mini_victorias_2T en un array de 3x3
        victoria_array = np.array([[a * 3 + b for b in range(3)] for a in range(3)], dtype=np.dtype('U2'))

        for (M_fila, M_columna) in self.mini_victorias_2T:
            victoria_array[M_fila, M_columna] = self.tablero[M_fila, M_columna, 0, 0, 0, 0]

        # Verificar filas
        for fila in victoria_array:
            if fila[0] == fila[1] == fila[2]:
                return (True, fila[0])

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

    def reinicio_3t(self):
        self.tablero = np.array([[[[[[str((v+1)+(u*3)) for v in range(3)] for u in range(3)] for j in range(3)] for i in range(3)] for t in range(3)] for k in range(3)],
                                dtype=np.dtype('U2'))
        self.mini_victorias_1T = []
        self.mini_victorias_2T = []

        self.num_mov = 0            # reiniciamos el número de movimientos
        self.cambiar_juginicial()          # cambiamos quién empieza en la nueva ronda
        self.actual = self.jugador_inicial  # y lo registramos

        self.restriccion = (-1, -1, -1, -1)  # el primer movimiento no tiene restricciones

    def update(self):
        """
        Actualiza el tablero, la puntuación y los botones en la pantalla, en el orden adecuado.
        """
        self.cursorEnCasilla()
        self.pantalla.blit(self.pantalla_trans,(0,0))
    
        self.dibujar_elementos()


###                   DIBUJO DEL DISPLAY - UI                  ###        
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

    def dibujar_3t(self):
        """
        Dibuja el tablero en la pantalla sollamente cuando se realice un movimiento.
        De esta forma se ahorran recursos y optimizamos nuestro juego
        """
        self.pantalla.blit(cte.fondo_3t,(0,0))
        for M_fila in range(3):
            for M_columna in range(3):
                for m_fila in range(3):
                    for m_columna in range(3):
                        for fila in range(3):
                            for columna in range(3):
        
                                match self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna]:
                                    case self.jugador1.simbolo:
                                        color = self.jugador1.color
                                    case self.jugador2.simbolo:
                                        color = self.jugador2.color
                                    case _:
                                        # Libre Movimiento - Todas: BLANCO_T
                                        if self.restriccion == (-1, -1, -1, -1):
                                            color = cte.BLANCO_T
                                        # Restricción 2T - Matriz 2T: BLANCO2_T
                                        elif self.restriccion[0] == M_fila and self.restriccion[1] == M_columna:
                                            color = cte.BLANCO2_T
                                            # Restricción 1T - Matriz 1T: BLANCO3_T
                                            if self.restriccion == (M_fila, M_columna, m_fila, m_columna):
                                                color = cte.BLANCO3_T

                                        # Restricción 2T no coincide con la casilla actual
                                        else:
                                            color = cte.BLANCO_T
                                # es una lsita hay que iterar o usar in
                                if (M_fila, M_columna) in self.mini_victorias_2T:
                                    tamaño = 234
                                    x = 310 + 250 * M_columna 
                                    y = -25 + 250 * M_fila 
                                elif (M_fila, M_columna, m_fila, m_columna) in self.mini_victorias_1T:
                                    tamaño = 78
                                    x = 290 + 242 * M_columna + 82 * m_columna
                                    y = -10 + 242 * M_fila + 80 * m_fila
                                else:
                                    tamaño = 26
                                    x = 282 + 242 * M_columna + 82 * m_columna + 80 / 3 * columna  # la 'x' se mueve por columnas
                                    y = -3 + 240 * M_fila + 80 * m_fila + 80 / 3 * fila  # la 'y' se mueve por filas

                                self.mostrar_texto(self.pantalla_trans, self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna],  cte.fuente_p1, tamaño, color, (x, y))

    def cursorEnCasilla(self):
            """
            Ilumina aquella casilla que el cursor está seleccionando
            Se está ejecutandose constantemente (tiene un único propósito para no ocasionar lag)
            """
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
                                            self.mostrar_texto(self.pantalla,self.tablero[M_fila, M_columna, m_fila, m_columna, fila, columna],cte.fuente_p1,26,cte.BLANCO,(x, y))

    def dibujar_elementos(self):
        """
        Dibuja los restantes elementos en la pantalla (botones y puntuación).
        Si el cursor se sitúa sobre un botón, este se iluminará. En caso contrario, permanecerá en reposo.
        """
        # PUNTUACIÓN
        # Símbolo del jugador
        self.mostrar_texto(self.pantalla,self.jugador1.simbolo, cte.fuente_p1, 45, self.jugador1.color,(69, 197))
        self.mostrar_texto(self.pantalla,self.jugador2.simbolo, cte.fuente_p1, 45, self.jugador2.color,(177, 197))     
        # Cantidad de Puntuación
        self.mostrar_texto(self.pantalla, str(self.jugador1.puntuacion), cte.fuente_p1, 45, cte.BLANCO,(73, 280))
        self.mostrar_texto(self.pantalla, str(self.jugador2.puntuacion), cte.fuente_p1, 45, cte.BLANCO,(181, 280))
        
        # BOTONES EN REPOSO - Transparentes
        # Salir
        pg.draw.rect(self.pantalla_trans, cte.verde_t3_T,(65,25,150,55))
        pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(65,25,150,55),2)
        self.mostrar_texto(self.pantalla_trans, 'SALIR', cte.fuente_p1, 20, cte.BLANCO2_T, (115,40))
        # Reiniciar
        pg.draw.rect(self.pantalla_trans, cte.verde_t3_T,(1065,25,150,55))
        pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(1065,25,150,55),2)
        self.mostrar_texto(self.pantalla_trans, 'REINICIAR', cte.fuente_p1, 20, cte.BLANCO2_T, (1100,40))      

        # BOTONES ILUMINADOS 
        m_pos = pg.mouse.get_pos()
        # Salir
        if 85 < m_pos[0] < 235 and 25 < m_pos[1] < 80:
            # Sólido
            pg.draw.rect(self.pantalla, cte.verde_t3,(65,25,150,55))
            pg.draw.rect(self.pantalla, cte.BLANCO,(65,25,150,55),2)
            self.mostrar_texto(self.pantalla, 'SALIR',cte.fuente_p1, 20, cte.BLANCO, (115,40))
        # Reiniciar
        if 1045 < m_pos[0] < 1195 and 25 < m_pos[1] < 80:
            pg.draw.rect(self.pantalla, cte.verde_t3,(1065,25,150,55))
            pg.draw.rect(self.pantalla, cte.BLANCO,(1065,25,150,55),2)
            self.mostrar_texto(self.pantalla, 'REINICIAR',cte.fuente_p1, 20, cte.BLANCO, (1100,40)) 