""" T2_settings.py

Este fichero contiene la creación de la clase Tablero 2. Además, en este script
se desarrollan todas las reglas y comprobaciones necesarias.

El fichero trabaja con el fichero/módulo llamado cte.py, donde se guardan todos los valores 
constantes como pueden ser los colores, las fuentes de letras, o rutas a determinadas imágenes.

Además, se utiliza el fichero/módulo Jugador.py, situado en la carpeta Settings, para importar la clase Jugador.

Para utilizar el código, es necesario tener instalada la librería pygame y la librería numpy en nuestro entorno virtual.
"""

# Módulos
import cte
from Settings.Jugador import Jugador

# Librerías
import pygame as pg
import numpy as np


class Tablero2:
    """
    Representa todas las configuraciones y reglas del Tablero1 (primer juego).
    
    Atributos
    ----------
    jugador1 : Jugador
        Instancia del primer jugador, especificamos todos sus atributos para este juego.
    jugador2 : Jugador
        Instancia del segundo jugador, especificamos todos sus atributos para este juego.
    pantalla : pygame.surface.Surface
        En ella mostramos todos los objetos pygame.
    pantalla_trans : pygame.surface.Surface
        Se trata como un rectángulo que admite opacidad y será mostrada mediante .blit() en pantalla.
    tablero : list of list
        Una lista de listas que forma el array 4D del tablero de juego, shape = (3, 3, 3, 3).
    actual : Jugador
        Define el jugador 'actual' que está jugando, contiene una referencia a la instancia del jugador.
    jugador_inicial : Jugador
        Define el jugador que realizará el primer movimiento, contiene una referencia a la instancia del jugador.

    Métodos
    -------
    __init__(self, pantalla, pantalla_trans)
        Inicializa la clase con los atributos especificados.
    cambiar_turno(self)
        Cambia el turno entre los jugadores.
    cambiar_juginicial(self)
        Alterna quién comienza en cada nueva partida.
    jugar_casilla(self, unicode)
        Actualiza el tablero cuando el jugador juega una casilla.
    definir_restriccion(self, m_fila, m_columna)
        Establece la restricción de movimiento para el rival
    matriz_ganada(self, matriz_f, matriz_c, ganador)
        Rellenamos toda una matriz de 3x3 con el simbolo ganador
    victoria_2t(self, tablero)
        Verifica si hay un ganador en el juego.
    reinicio_2t(self)
        Reinicia el tablero y otros atributos para un nuevo juego.
    update(self)
        Actualiza el tablero, la puntuación y los botones en la pantalla, en el orden adecuado.
    mostrar_texto(self, pantalla_int, texto, fuente, tamaño, color, posicion)
        Muestra un texto en la pantalla.
    dibujar_2t(self)
        Dibuja el tablero en la pantalla.
    dibujar_elementos(self)
        Dibuja todos los elementos decorativos en la pantalla.
    """
    def __init__(self, pantalla, pantalla_trans):


        # Instancias iniciales
        self.jugador1 = Jugador('Jug1','X', 0, cte.amarillo_t2)
        self.jugador2 = Jugador('Jug2', 'o', 0, cte.gris_t2)
        self.pantalla = pantalla 
        self.pantalla_trans = pantalla_trans

        # Atributos de configuraciones / juego
        """
        Numpy trata las cadenas de caracteres como matrices de caracteres Unicode.
        Por tanto, tendremos que especificar la longitud de datos usando np.dtype('UX'), donde X es la longitud.

        Referencias:
        Usuario anjaneyulubatta505. (2019). Numpy taking only first character of string (Respuesta a la publicación). 
        https://stackoverflow.com/questions/55377213/numpy-taking-only-first-character-of-string
        """
        self.tablero = np.array([[[['0' for j in range(3)] for i in range(3)] for t in range(3)] for k in range(3)], 
                                dtype=np.dtype('U2')) # Establecemos la longitud de datos hasta 2 (usaremos 'J1' y 'J2')
        """
        i → filas                 para acceder a un elemento → [k, t, i, j],
        j → columnas              equivale a → [matriz_f, matriz_c, fila, columna]
        k → matriz_f
        t → matriz_c

        str((j*1)+(i*9)+(t*3)+(k*27) + 1)     # matriz del 1 al 81
        str((j+1)+(i*3))                      # matriz del 1 al 9, 9 veces
        np.dtype('U'+str(max([len(self.jugador1.simbolo), len(self.jugador2.simbolo)])))) → longitud adaptada a cualquier simbolo
        """

        self.actual = self.jugador1     
        self.jugador_inicial = self.jugador1
        self.numero_movimientos = 0

        self.mini_victorias = []     # guarda aquellas matrices de 3x3 ganadas
        self.restriccion = (-1,-1)      # guarda la restricción en un formato (matriz_f, matriz_c)
                                        # (-1, -1) indica que no hay restricción de movimiento


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

    def definir_restriccion(self, m_fila:int, m_columna:int):
        """
        Establece la restricción de movimiento para el rival

        Parámetros
        ---------
        m_fila: int
            Representa la fila jugada, se transforma en m_fila
        m_columna: int
            Representa la columna jugada, se transforma en m_columna
        """
        # Matriz libre
        if (m_fila, m_columna) not in self.mini_victorias:
            self.restriccion = (m_fila, m_columna)   
            self.cambiar_turno()
        # Matriz completada
        else:
            self.restriccion = (-1, -1)
            self.cambiar_turno()    


###                   COMPROBACIONES Y ACTUALIZACIONES               ###

    def jugar_casilla(self, unicode:int|bool):
        """
        Actualiza la casilla del tablero según la jugada realizada por el usuario.

        Parámetros
        ----------
        unicode : bool|int
            Si es un entero, representa la casilla de la tecla presionada. Si es False, se usa la posición del mouse para determinar la casilla.
        """

        # Usamos las teclas
        if unicode:
            # Transformación de tecla a: fila y columna
            fila = (unicode - 1) // 3 
            columna = (unicode - 1) % 3

            matriz_f, matriz_c = self.restriccion    # desempaquetamos la tupla de restriccion
            
            # El tablero de la casilla jugada no ha sido ganado
            if (matriz_f, matriz_c) not in self.mini_victorias:
                # Al jugador se le permitía jugar donde quiere (-1, -1)
                if self.restriccion == (-1, -1):
                    pass    # Tendríamos que especificar que mamtriz queremos jugar (necesitamos más teclas para esto)
                
                # Al jugador se le obligaba a jugar en la tupla: restriccion 
                else:
                    # La casilal está sin jugar
                    if self.tablero[self.restriccion[0], self.restriccion[1], fila, columna] == '0':
                        self.tablero[matriz_f, matriz_c, fila, columna] = self.actual.simbolo       # 1º Actualizamos tablero
                        self.mini_victorias = self.get_mini_victorias()                  # 2º Obtenemos las mini_victorias actuales
                        self.definir_restriccion(fila, columna)     # 3º Añadimos las oportunas restricciones       
                        self.numero_movimientos += 1                                # para el próximo jugador

        # Usamos el mosue         
        else:
            m_pos = pg.mouse.get_pos()
            for matriz_f in range(3):
                for matriz_c in range(3):
                    for fila in range(3):
                        for columna in range(3):
                    
                            if self.restriccion == (-1, -1): 
                                x = 350 + 200*matriz_c+columna*200/3    # la 'x' se mueve por columnas
                                y = 110 + 200*matriz_f+fila*200/3       # la 'y' se mueve por filas
                                                    
                            else:
                                x = 350 + 200*self.restriccion[1]+columna*200/3  # matriz_c ya está definida por la restricción
                                y = 110 + 200*self.restriccion[0]+fila*200/3     # matriz_f ya está definida por la restricción

                            # Calculamos la posición de cada número
                            if x < m_pos[0] < x+200/3  and y < m_pos[1] < y+200/3:
                                # El tablero de la casilla jugada no ha sido ganado
                                if (matriz_f, matriz_c) not in self.mini_victorias:
                                    # Al jugador se le permitía jugar donde quiere (-1, -1)
                                    if self.restriccion == (-1, -1):
                                        # La casilla está sin jugar
                                        if self.tablero[matriz_f, matriz_c, fila, columna] == '0':
                                            self.tablero[matriz_f, matriz_c, fila, columna] = self.actual.simbolo       # 1º Actualizamos tablero
                                            self.mini_victorias = self.get_mini_victorias()                  # 2º Obtenemos las mini_victorias actuales
                                            self.definir_restriccion(fila, columna)     # 3º Añadimos las oportunas restricciones
                                            self.numero_movimientos += 1                                # para el próximo jugador
                                                                                                        

                                    # Al jugador se le obligaba a jugar en la tupla: restriccion   
                                    else:
                                        # La casilla está sin jugar
                                        if self.tablero[self.restriccion[0], self.restriccion[1], fila, columna] == '0':
                                            self.tablero[self.restriccion[0], self.restriccion[1], fila, columna] = self.actual.simbolo
                                            self.mini_victorias = self.get_mini_victorias()                        
                                            self.definir_restriccion(fila, columna)
                                            self.numero_movimientos += 1

    def matriz_ganada(self, matriz_f:int, matriz_c:int, ganador:str):
        """
        Rellenamos toda una matriz de 3x3 con el simbolo ganador

        Parámetros
        ----------
        matriz_f: int
            Representa la fila de la matriz grande
        matriz_c: int
            Representa la columna de la matriz grande
        ganador: str
            Representa el símbolo del jugador que ganó la matriz grande
        """        
        for fila_n in range(3):
            for columna_n in range(3):
                self.tablero[matriz_f, matriz_c, fila_n, columna_n] =  ganador
                        
    def get_mini_victorias(self):
        """
        Se estará ejecutando dentró del bucle del juego (se actualiza  en cada iteración)
        Registra condiciones de victoria dentro de cada matriz 3x3 (al igual que en T1, solo que ahora son 9 matrices)
        """

        mini_victorias = []

        # Iteramos las 9 matrices grandes
        for matriz_f in range(3):
            for matriz_c in range(3):

                matriz_2t = self.tablero[matriz_f, matriz_c] # toma el valor de cada matriz grande (2T)

                # Verificar filas
                for fila in matriz_2t:
                    if fila[0] == fila[1] == fila[2] != '0':
                        self.matriz_ganada(matriz_f, matriz_c, fila[0]) # rellenamos la matriz con el símbolo del ganador
                        mini_victorias.append((matriz_f, matriz_c))     # añadimos la matriz ganada a mini_victorias

                # Verificar columnas
                for columna in range(3):
                    if matriz_2t[0, columna] == matriz_2t[1, columna] == matriz_2t[2, columna] != '0':
                        self.matriz_ganada(matriz_f, matriz_c, self.tablero[matriz_f, matriz_c, 0, columna])
                        mini_victorias.append((matriz_f, matriz_c))
                    
                # Verificar diagonales
                if matriz_2t[0, 0] == matriz_2t[1, 1] == matriz_2t[2, 2] != '0':
                    self.matriz_ganada(matriz_f, matriz_c, self.tablero[matriz_f, matriz_c, 0, 0])
                    mini_victorias.append((matriz_f, matriz_c))
                    
                if matriz_2t[0, 2] == matriz_2t[1, 1] == matriz_2t[2, 0] != '0':
                    self.matriz_ganada(matriz_f, matriz_c, self.tablero[matriz_f, matriz_c, 0, 2])
                    mini_victorias.append((matriz_f, matriz_c))
                
        return mini_victorias

    def victoria_2t(self):
        """
        Verifica si hay un ganador en el juego

        Devuelve
        --------
        tuple
            Devuelve una tupla con un valor booleano (indica si hay victoria)
            y el símbolo del ganador de la partida

        """
        victoria_array = np.array([['0' for j in range(3)] for i in range(3)], dtype=np.dtype('U2'))

        for (fila, columna) in self.mini_victorias:
            victoria_array[fila, columna] = self.tablero[fila, columna, 0, 0] # rellenamos cada casilla de la nueva matriz con el simbolo del ganador

        # Verificar filas
        for fila in victoria_array:
            if fila[0] == fila[1] == fila[2] != '0':
                return (True, fila[0])

        # Verificar columnas
        for columna in range(3):
            if victoria_array[0, columna] == victoria_array[1, columna] == victoria_array[2, columna] != '0':
                return (True, victoria_array[0, columna])  
                    
        # Verificar diagonales
        if victoria_array[0, 0] == victoria_array[1, 1] == victoria_array[2, 2] != '0':
            return (True, victoria_array[0, 0])
           
        if victoria_array[0, 2] == victoria_array[1, 1] == victoria_array[2, 0] != '0':
            return (True, victoria_array[0, 2])         
          
        return (False, None)

    def reinicio_2t(self):
        """
        Reinicia el tablero y otros atributos para un nuevo juego.
        """
        self.tablero = np.array([[[['0' for j in range(3)] for i in range(3)] for t in range(3)] for k in range(3)], 
                                dtype=np.dtype('U2'))

        self.cambiar_juginicial()           # cambiamos quién empieza en la nueva ronda 
        self.actual = self.jugador_inicial  # y lo registramos
        self.restriccion = (-1, -1)         # el primer movimiento no tiene restricciones
        self.mini_victorias = []

    def update(self):
        """
        Actualiza el tablero, la puntuación y los botones en la pantalla, en el orden adecuado.
        """
        self.dibujar_2t()

        self.pantalla.blit(self.pantalla_trans, (0,0))
        self.pantalla_trans.fill((0, 0, 0, 0))
    
        self.dibujar_elementos()


###                   DIBUJO DEL DISPLAY - UI                  ###

    def mostrar_texto(self, pantalla_int, texto:str, fuente, tamaño:int, color:tuple|str, posicion:tuple):
        """
      Muestra un texto en la pantalla.

      Parámetros
      ----------
      pantalla_int : pygame.surface.Surface
          La pantalla en la que se mostrará el texto.
      texto : str
          El texto a mostrar.
      fuente : str
          La fuente del texto.
      tamaño : int
          El tamaño del texto.
      color : tuple | str
          El color del texto. Admite hexadecimal y RGB/RGBA
      posicion : tuple
          La posición del texto en la pantalla.
      """
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

    def dibujar_2t(self):
        """
        Dibuja el tablero en la pantalla.
        """
        self.pantalla.blit(cte.fondo_2t,(0,0))
        for matriz_f in range(3):
            for matriz_c in range(3):
                for fila in range(3):
                    for columna in range(3):
                        
                        m_pos = pg.mouse.get_pos()
                        #print(self.tablero)
                        x = 350 + 200*matriz_c+columna*200/3    # la 'x' se mueve por columnas
                        y = 110 + 200*matriz_f+fila*200/3       # la 'y' se mueve por filas

                        # Dibujar matriz con minivictoria
                        if (matriz_f, matriz_c) in self.mini_victorias:

                            color = self.jugador1.color if self.tablero[matriz_f, matriz_c, 0, 0] == self.jugador1.simbolo else self.jugador2.color

                            self.mostrar_texto(self.pantalla,self.tablero[matriz_f, matriz_c, 0, 0],cte.fuente_p1,120,color,
                                                   (390 + 200*matriz_c,115 + 190*matriz_f))
                                
                        # Dibujar matriz sin minivictoria
                        else:
                            if self.tablero[matriz_f, matriz_c, fila, columna] == self.jugador1.simbolo:
                                self.mostrar_texto(self.pantalla,self.tablero[matriz_f, matriz_c, fila, columna],cte.fuente_p1,35,self.jugador1.color,(x+10, y))
                                                
                            elif self.tablero[matriz_f, matriz_c, fila, columna] == self.jugador2.simbolo:
                                self.mostrar_texto(self.pantalla,self.tablero[matriz_f, matriz_c, fila, columna],cte.fuente_p1,35,self.jugador2.color,(x+10, y))
                            
                            # Casillas no jugadas
                            else:
                                # Cursor encima
                                if x < m_pos[0] < x+200/3  and y < m_pos[1] < y+200/3:
                                    self.mostrar_texto(self.pantalla,str(1 + fila*3 + columna),cte.fuente_p1,35,cte.BLANCO,(x+10, y))
                                # Casillas sin cursor
                                else:
                                    if matriz_f == self.restriccion[0] and matriz_c == self.restriccion[1]:
                                        self.mostrar_texto(self.pantalla_trans,str(1 + fila*3 + columna),cte.fuente_p1,35,cte.BLANCO3_T,(x+10, y))
                                    # Incluye self.restriccion (-1, -1 → nunca coincide)
                                    else:
                                        self.mostrar_texto(self.pantalla_trans,str(1 + fila*3 + columna),cte.fuente_p1,35,cte.BLANCO_T,(x+10, y))                                        

    def dibujar_elementos(self):
        """
        Dibuja los restantes elementos en la pantalla (botones y puntuación).
        Si el cursor se sitúa sobre un botón, este se iluminará. En caso contrario, permanecerá en reposo.
        """
        # PUNTUACIÓN
        # Símbolo del jugador
        self.mostrar_texto(self.pantalla,self.jugador1.simbolo, cte.fuente_p1, 35, cte.BLANCO,(90, 300))
        self.mostrar_texto(self.pantalla,self.jugador2.simbolo, cte.fuente_p1, 35, cte.BLANCO,(210, 300))     
        # Cantidad de Puntuación
        self.mostrar_texto(self.pantalla, str(self.jugador1.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(95, 390))
        self.mostrar_texto(self.pantalla, str(self.jugador2.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(215, 390))
        
        # BOTONES EN REPOSO - Transparentes
        # Salir
        pg.draw.rect(self.pantalla_trans, cte.naranja_t2_T,(85,25,150,55))
        pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(85,25,150,55),2)
        self.mostrar_texto(self.pantalla_trans, 'SALIR', cte.fuente_p1, 20, cte.BLANCO2_T, (135,40))
        # Reiniciar
        pg.draw.rect(self.pantalla_trans, cte.naranja_t2_T,(1045,25,150,55))
        pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(1045,25,150,55),2)
        self.mostrar_texto(self.pantalla_trans, 'REINICIAR', cte.fuente_p1, 20, cte.BLANCO2_T, (1080,40))      

        # BOTONES ILUMINADOS 
        m_pos = pg.mouse.get_pos()
        # Salir
        if 85 < m_pos[0] < 235 and 25 < m_pos[1] < 80:
            # Sólido
            pg.draw.rect(self.pantalla, cte.naranja_t2,(85,25,150,55))
            pg.draw.rect(self.pantalla, cte.BLANCO,(85,25,150,55),2)
            self.mostrar_texto(self.pantalla, 'SALIR',cte.fuente_p1, 20, cte.BLANCO, (135,40))
        # Reiniciar
        if 1045 < m_pos[0] < 1195 and 25 < m_pos[1] < 80:
            pg.draw.rect(self.pantalla, cte.naranja_t2,(1045,25,150,55))
            pg.draw.rect(self.pantalla, cte.BLANCO,(1045,25,150,55),2)
            self.mostrar_texto(self.pantalla, 'REINICIAR',cte.fuente_p1, 20, cte.BLANCO, (1080,40))  
