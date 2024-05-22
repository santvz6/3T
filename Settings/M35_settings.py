""" M35_settings.py

Este fichero contiene la creación de la clase M35. Además, en este script
se desarrollan todas las reglas y comprobaciones necesarias.

El fichero trabaja con el fichero/módulo llamado cte.py, donde se guardan todos los valores 
constantes como pueden ser los colores, las fuentes de letras, o rutas a determinadas imágenes.

Además, se utiliza el fichero/módulo Jugador.py, situado en la carpeta Settings, para importar la clase Jugador.

Para utilizar el código, es necesario tener instalada la librería pygame y la librería re en nuestro entorno virtual.
"""

# Librerías
import pygame as pg
import re

# Ficheros
import cte
from Settings.Jugador import Jugador


class M35:
    """
    Representa todas las configuraciones y reglas del M35 (cuarto juego).
    
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
    _tablero : list of list
        Una lista de listas que forma el array 2D del tablero de juego, shape = (5, 5).
    _actual : Jugador
        Define el jugador 'actual' que está jugando, contiene una referencia a la instancia del jugador.
    _jugador_inicial : Jugador
        Define el jugador que realizará el primer movimiento, contiene una referencia a la instancia del jugador.
    transparencia : int
        Define el nivel de transparencia de la pantalla_trans.
    num_movimientos: int
        Se guarda el número de movimientos realizados en toda la partida. Sirve como condición de empate

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
    victoria_m35(self, tablero)
        Verifica si hay un ganador en el juego.
    restringir(self)
        Limita el lugar del tablero donde se podrá realizar el próximo movimiento
    reinicio_m35(self)
        Reinicia el tablero y otros atributos para un nuevo juego.
    mostrar_texto(self, pantalla_int, texto, fuente, tamaño, color, posicion)
        Muestra un texto en la pantalla.
    dibujar_m35(self)
        Dibuja el tablero en la pantalla.
    dibujar_elementos(self)
        Dibuja todos los elementos decorativos en la pantalla.
    actualizar_m35_mouse
         Permite al jugador colocar ficha en una casilla si no esta ocupada
     transicion(self)
        Realiza una transición de opacidad en la pantalla.
    update(self)
        Actualiza el tablero, la puntuación y los botones en la pantalla, en el orden adecuado.
    """
    def __init__(self, pantalla, pantalla_trans):
        """
        Inicializa la clase con los atributos especificados.
        Parámetros
        ----------
        pantalla : pygame.surface.Surface
            En ella mostramos todos los objetos pygame.
        pantalla_trans : pygame.surface.Surface
            Se trata como un rectángulo que admite opacidad y será mostrada mediante .blit() en pantalla.
        """
        # Creación del tablero
        self.tablero = [[str((n+1)+(m*5)) for n in range(5)] for m in range(5)]

        #print(self.tablero)

        # Instancias iniciales
        self.jugador1 = Jugador('Jug1','J1', 0, cte.amarillo_t1)
        self.jugador2 = Jugador('Jug2', 'J2', 0, cte.azul_1)

        # Atributos de instancia
        self.pantalla = pantalla 
        self.pantalla_trans = pantalla_trans
        self.actual = self.jugador1 # Primer movimiento
        self.jug_ini = self.jugador1 # Cambio de
        self.restriccion = []
        self.transparencia = 255
        self.num_mov = 0

########################### LÓGICA DEL JUEGO ORIENTADA A PYTHON VANILLA ###########################

    def cambiar_turno(self):
        '''
            Intercambia el jugador actual
        '''
        self.actual = self.jugador1 if self.jugador2 == self.actual else self.jugador2
        
        
    def jug_inicial(self):
        '''
            Jugador que empieza la partida
        '''
        self.jug_ini = self.jugador1 if self.jugador2 == self.jug_ini else self.jugador2

    def victoria_m35(self):
        """
        Verifica si hay un ganador en el juego.

        Parámetros
        ----------
        tablero : list of list
            El tablero de juego.
        simb_prev : str
            El último jugador en poner ficha
        comb_ganadora : 
            Es la combinación que se da para ganar (alineacion de un jugador)
        filas : str
            Revisa las filas en busca de comb_ganadora
        columnas : str
            Revisa las columnas en busca de comb_ganadora
        diagonal : str
            Revisa las diagonales de izq a der en busca de comb_ganadora
        diagonal2 : str
            Revisa las diagonales de der a izq en busca de comb_ganadora
        Devuelve
        -------
        tuple
            Una tupla que contiene un booleano indicando si hay un ganador y el símbolo del ganador.
        """
        if self.actual.simbolo == 'J1':
            simb_prev = 'J2'
        else:
            simb_prev = 'J1'
        
        comb_ganadora = simb_prev*3
    # Verificar filas
        for fila in self.tablero:
            self.filas = ''
            for n in range(5):
                self.filas += str(fila[n])

            if re.search(comb_ganadora, self.filas):
                return (True, simb_prev)

    # Verificar columnas
        for n in range(5):
            self.columnas = ''
            for columna in self.tablero:
                self.columnas += str(columna[n])

            if re.search(comb_ganadora, self.columnas):
                return (True, simb_prev)

    # Verificar diagonales
    # Izq - der
        for i in range(5):
            inicio = 6
            final = 6
            self.diagonal = ''
            match i:
                case 0:
                    inicio = 0
                    final = 5
                case 1:
                    inicio = 0
                    final = 4
                case 2:
                    inicio = 0
                    final = 3
                case 3:
                    inicio = 2
                    final = 5
                case 4:
                    inicio = 1
                    final = 5

            for j in range(inicio, final, 1):
                self.diagonal += str(self.tablero[j][(i+j)%5])
            
            if re.search(comb_ganadora, self.diagonal):
                return (True, simb_prev)
        
    #Der - izq
        for i in range(5):
            inicio = 6
            final = 6
            self.diagonal2 = ''
            
            match i:
                case 0:
                    inicio = 5
                    final = 0
                case 1:
                    inicio = 4
                    final = 0
                case 2:
                    inicio = 3
                    final = 0
                case 3:
                    inicio = 5
                    final = 2
                case 4:
                    inicio = 5
                    final = 1

            for j in range(inicio, final, -1):
                self.diagonal2 += str(self.tablero[j-1][-(j-5+i)])
    
            if re.search(comb_ganadora, self.diagonal2):
                return (True, simb_prev)
        
        return (False, None)

    def restringir(self, centro):
        '''
            Restringe donde el jugador actual puede hacer su movimiento
        '''
        self.restriccion = []
        self.centro = centro
        self.fila = self.centro[0]
        self.columna = self.centro[1]

        
        for i in range(-1, 2):
            for j in range(-1, 2):
                fila_restringida = self.fila + i
                columna_restringida = self.columna + j
                match fila_restringida:
                    case -1:
                        fila_restringida = 4
                    case 5:
                        fila_restringida = 0
                    
                match columna_restringida:
                    case -1:
                        columna_restringida = 4
                    case 5:
                        columna_restringida = 0
            
                self.restriccion.append((fila_restringida, columna_restringida))
        return self.restriccion 
    

    def reinicio_m35(self):
        """
        Reinicia el tablero y otros atributos para un nuevo juego y cambiamos el jugador inicial de la nueva ronda.
        """
        self.tablero = [[str((n+1)+(m*5)) for n in range(5)] for m in range(5)]
        self.num_mov = 0
        self.restriccion = []
        self.jug_inicial()
        self.actual = self.jug_ini
        self.transparencia = 255
                

########################### LÓGICA DEL JUEGO ORIENTADA A PYGAME ###########################


    def mostrar_texto(self,pantalla_int, texto, fuente, tamaño, color, posicion):
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
            text_surface.set_alpha(color[3])  # render elimina la opacidad
            self.pantalla_trans.blit(text_surface, text_rect)

        elif pantalla_int == self.pantalla:
            self.pantalla.blit(text_surface, text_rect)

    def dibujar_m35(self):
        """
        Dibuja cada casilla del tablero según unas condiciones especificas.
        """
        self.pantalla.blit(cte.fondo_m35,(0,0))
        for fila in range(5):
            for columna in range(5):
                m_pos = pg.mouse.get_pos()

                match self.tablero[fila][columna]:
                    # Los símbolos de los jugadores siempre estarán iluminados
                    case self.jugador1.simbolo:
                        self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,self.jugador1.color,(410+110*columna,165+110*fila))
                    case self.jugador2.simbolo:
                        self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,self.jugador2.color,(410+110*columna,165+110*fila))
                    # Las casillas sin jugar no siempre estarán iluminadas
                    case _:
                        # el cursor está encima → lo iluminamos de blanco
                        if 355+115*(columna) < m_pos[0] < 355+115*(columna+1) and 120+115*fila < m_pos[1] < 120+115*(fila+1):
                            self.mostrar_texto(self.pantalla,str(1 +fila*5 + columna),cte.fuente_p1,35,cte.BLANCO,(410+110*columna,165+110*fila))
                        # el cursor no está encima → lo coloreamos de blanco transparente
                        else:
                            self.mostrar_texto(self.pantalla_trans,str(1 +fila*5 + columna),cte.fuente_p1,35,cte.BLANCO_T,(410+110*columna,165+110*fila))
            
    def dibujar_elementos(self):
        """
        Dibuja los restantes elementos en la pantalla (botones y puntuación).
        Si el cursor se sitúa sobre un botón, este se iluminará. En caso contrario, permanecerá en reposo.
        """
        m_pos = pg.mouse.get_pos()
        # Simbolo
        self.mostrar_texto(self.pantalla,self.jugador1.simbolo, cte.fuente_p1, 35, cte.BLANCO,(1025, 600))
        self.mostrar_texto(self.pantalla,self.jugador2.simbolo, cte.fuente_p1, 35, cte.BLANCO,(1200, 600))
        # Separador
        self.mostrar_texto(self.pantalla,':', None, 35, cte.BLANCO,(1055, 610))
        self.mostrar_texto(self.pantalla,'-', None, 35, cte.BLANCO,(1115, 610))
        self.mostrar_texto(self.pantalla,':', None, 35, cte.BLANCO,(1185, 610))
        # Puntuación
        self.mostrar_texto(self.pantalla, str(self.jugador1.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(1080, 600))
        self.mostrar_texto(self.pantalla, str(self.jugador2.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(1145, 600))
        # Salir
        pg.draw.rect(self.pantalla_trans, cte.amarillo_t1_T,(50,25,150,55))
        pg.draw.rect(self.pantalla_trans, cte.BLANCO_T,(50,25,150,55),2)
        self.mostrar_texto(self.pantalla_trans, 'SALIR', cte.fuente_p1, 20, cte.BLANCO_T, (100,40))
        self.pantalla.blit(self.pantalla_trans, (0,0))
        # Salir_on
        if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
            pg.draw.rect(self.pantalla, cte.amarillo_t1,(50,25,150,55))
            pg.draw.rect(self.pantalla, cte.BLANCO,(50,25,150,55),2)
            self.mostrar_texto(self.pantalla, 'SALIR',cte.fuente_p1, 20, cte.BLANCO, (100,40))
        # Reniciar
        pg.draw.rect(self.pantalla_trans, cte.amarillo_t1_T,(1080,25,150,55))
        pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(1080,25,150,55),2)
        self.mostrar_texto(self.pantalla_trans, 'REINICIAR', cte.fuente_p1, 20, cte.BLANCO2_T, (1115,40))
        # Reiniciar_on
        if 1080 < m_pos[0] < 1230 and 25 < m_pos[1] < 80:
            pg.draw.rect(self.pantalla, cte.amarillo_t1,(1080,25,150,55))
            pg.draw.rect(self.pantalla, cte.BLANCO,(1080,25,150,55),2)
            self.mostrar_texto(self.pantalla, 'REINICIAR',cte.fuente_p1, 20, cte.BLANCO, (1115,40))
        

        for casillas in self.restriccion:
            if self.tablero[casillas[0]][casillas[1]] in [str(_ + 1) for _ in range(25)]: 
                self.mostrar_texto(self.pantalla_trans,str(1 +casillas[0]*5 + casillas[1]),cte.fuente_p1,35,(255, 255, 255, 130),(410+110*casillas[1],165+110*casillas[0]))            


    def actualizar_m35_mouse(self):
        '''
            Permite al jugador colocar ficha en una casilla si no esta ocupada
        '''
        m_pos = pg.mouse.get_pos()
        for x in range(5):
            for y in range(5):
                if 355+115*(y) < m_pos[0] < 355+115*(y+1) and 120+115*x < m_pos[1] < 120+115*(x+1):
                    return (x, y)
        return False

                
                
    def validar(self, centro):          
        # Validación casilla sin jugar
        x = centro[0]
        y = centro[1]
        if self.tablero[x][y] in [str(_ + 1) for _ in range(25)]:
            self.tablero[x][y] = self.actual.simbolo
            self.cambiar_turno()
            self.num_mov += 1
            self.restriccion = self.restringir(centro)


    def transicion(self):
        """
        Realiza una transición de opacidad en la pantalla.
        """
        if self.transparencia > 0:
            self.transparencia -= 5

        pg.draw.rect(self.pantalla_trans, (0,0,0,self.transparencia), (0,0,1280, 720))
        self.pantalla.blit(self.pantalla_trans, (0,0))



########################### TRAS UNA JUGADA VÁLIDA ###########################   
    def update(self):
        """
        Actualiza el tablero, la puntuación y los botones en la pantalla, en el orden adecuado.

        El método update será ejecutado en el bucle while del juego constantemente.
        """
        self.dibujar_m35()  # Fondo y tablero
        self.pantalla.blit(self.pantalla_trans, (0,0))
        self.pantalla_trans.fill((0,0,0,0))
        self.dibujar_elementos()  # Elementos
        
        
