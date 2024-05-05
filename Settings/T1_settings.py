""" T1_settings.py

Este fichero contiene la creación de la clase Tablero 1. Además, en este script
se desarrollan todas las reglas y comprobaciones necesarias.

El fichero trabaja con el fichero/módulo llamado cte.py, donde se guardan todos los valores 
constantes como pueden ser los colores, las fuentes de letras, o rutas a determinadas imágenes.

Además, se utiliza el fichero/módulo Jugador.py, situado en la carpeta Settings, para importar la clase Jugador.

Para utilizar el código, es necesario tener instalada la librería pygame en nuestro entorno virtual.

El fichero puede ser importado como módulo y contiene las siguientes funciones:

    * victoria_1t - devuelve un valor Bool dependiendo del estado del tablero
    * tablero_full - devuelve un valor Bool dependiendo del estado del tablero
    * update - ejecuta el dibujo de la UI de manera eficaz
"""

# Módulos
import cte
from Settings.Jugador import Jugador

# Librerías
import pygame as pg

class Tablero1:
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
      Una lista de listas que forma el array 2D del tablero de juego, shape = (3, 3).
  actual : Jugador
      Define el jugador 'actual' que está jugando, contiene una referencia a la instancia del jugador.
  jugador_inicial : Jugador
      Define el jugador que realizará el primer movimiento, contiene una referencia a la instancia del jugador.
  transparencia : int
      Define el nivel de transparencia de la pantalla_trans.

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
  victoria_1t(self, tablero)
      Verifica si hay un ganador en el juego.
  tablero_full(self, tablero)
      Verifica si el tablero está lleno.
  reinicio_1t(self)
      Reinicia el tablero y otros atributos para un nuevo juego.
  update(self)
      Actualiza el tablero, la puntuación y los botones en la pantalla, en el orden adecuado.
  mostrar_texto(self, pantalla_int, texto, fuente, tamaño, color, posicion)
      Muestra un texto en la pantalla.
  dibujar_1t(self)
      Dibuja el tablero en la pantalla.
  transicion(self)
      Realiza una transición de opacidad en la pantalla.
  dibujar_elementos(self)
      Dibuja todos los elementos decorativos en la pantalla.
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
      # Instancias iniciales
      self.jugador1 = Jugador('Jug1','J1', 0, cte.amarillo_t1)
      self.jugador2 = Jugador('Jug2', 'J2', 0, cte.azul_1)
      self.pantalla = pantalla 
      self.pantalla_trans = pantalla_trans
      # Atributos de configuraciones / juego
      self.tablero = [['0' for j in range(3)] for i in range(3)] # Creación del tablero
      self.actual = self.jugador1
      self.jugador_inicial = self.jugador1
      self.transparencia = 255


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


###                   COMPROBACIONES Y ACTUALIZACIONES               ###

  def jugar_casilla(self, unicode):
      """
      Actualiza la casilla del tablero según la jugada realizada por el usuario.

      Parámetros
      ----------
      unicode : bool|int
          Si es un entero, representa la casilla de la tecla presionada. Si es False, se usa la posición del mouse para determinar la casilla.
      """
      
      if unicode:
          # Transformación de tecla a: fila y columna
          fila = (unicode - 1) // 3 
          columna = (unicode - 1) % 3
          if self.tablero[fila][columna] == '0':
              self.tablero[fila][columna] = self.actual.simbolo
              self.cambiar_turno()
      else:
          m_pos = pg.mouse.get_pos()
          for fila in range(3):
              for columna in range(3):
                  if self.tablero[fila][columna] == '0':
                      if 532+80.6*(columna) < m_pos[0] < 524+80.6*(columna+1) and 240+80*fila < m_pos[1] < 240+80.6*(fila+1):          
                          self.tablero[fila][columna] = self.actual.simbolo
                          self.mostrar_texto(self.pantalla,str(self.tablero[fila][columna]),cte.fuente_p1,35,self.actual.color,(560+80*columna,259+80*fila))
                          self.cambiar_turno()
  
  def victoria_1t(self, tablero):
      """
      Verifica si hay un ganador en el juego.

      Parámetros
      ----------
      tablero : list of list
          El tablero de juego.

      Devuelve
      -------
      tuple
          Una tupla que contiene un booleano indicando si hay un ganador y el símbolo del ganador.
      """
      # Verificar filas
      for fila in tablero:
          if fila[0] == fila[1] == fila[2] != '0':
              return True, fila[0]
      # Verificar columnas
      for columna in range(3):
          if tablero[0][columna] == tablero[1][columna] == tablero[2][columna] != '0':
              return (True, tablero[0][columna])
      # Verificar diagonales
      if tablero[0][0] == tablero[1][1] == tablero[2][2] != '0':
          return (True, tablero[0][0])
      if tablero[0][2] == tablero[1][1] == tablero[2][0] != '0':
          return (True, tablero[0][2])
      return (False, None)
  
  def tablero_full(self, tablero):
      """
      Verifica si el tablero está lleno.

      Parámetros
      ----------
      tablero : list of list
          El tablero de juego.

      Devuelve
      -------
      bool
          True si el tablero está lleno, False de lo contrario.
      """
      for fila in tablero:
          if fila.count('0') == 0:
              return True
      return False
  
  def reinicio_1t(self):
      """
      Reinicia el tablero y otros atributos para un nuevo juego y cambiamos el jugador inicial de la nueva ronda.
      """
      self.tablero = [['0' for j in range(3)] for i in range(3)]
      self.cambiar_juginicial()
      self.transparencia = 255

  def update(self):
      """
      Actualiza el tablero, la puntuación y los botones en la pantalla, en el orden adecuado.

      El método update será ejecutado en el bucle while del juego constantemente.
      """

      self.dibujar_1t()
      self.pantalla.blit(self.pantalla_trans, (0,0))
      self.pantalla_trans.fill((0, 0, 0, 0)) # limpiamos la superficie transparente, sino se acumulan y pierde la transparencia
      self.dibujar_elementos()


###                   DIBUJO DEL DISPLAY - UI                  ###
  def mostrar_texto(self, pantalla_int, texto:str, fuente:str, tamaño:int, color:str|tuple, posicion:tuple):
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
      font = pg.font.Font(fuente, tamaño)             # cargamos la fuente
      text_surface = font.render(texto, True, color)  # creamos el texto con Anti-Aliasing y el color especificado
      
      text_rect = text_surface.get_rect() # obtenemos el rectángulo del text usando .get_rect()
      text_rect.topleft = posicion        # situamos la parte superior izquierda en las coordenadas de posicion
      
      # Dependiendo de la pantalla, tratamos RGB o RGBA
      if pantalla_int == self.pantalla_trans:
          text_surface.set_alpha(color[3]) # RGBA
          self.pantalla_trans.blit(text_surface, text_rect)
      elif pantalla_int == self.pantalla:
          self.pantalla.blit(text_surface, text_rect) # RGB

  def dibujar_1t(self):
      """
      Dibuja cada casilla del tablero según unas condiciones especificas.
      """
      self.pantalla.blit(cte.fondo_1t,(0,0))
      for fila in range(3):
          for columna in range(3):
              m_pos = pg.mouse.get_pos()

              match self.tablero[fila][columna]:
                  # Los símbolos de los jugadores siempre estarán iluminados
                  case self.jugador1.simbolo:
                      self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,self.jugador1.color,(560+80*columna,259+80*fila))
                  case self.jugador2.simbolo:
                      self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,self.jugador2.color,(560+80*columna,259+80*fila))
                  # Las casillas sin jugar no siempre estarán iluminadas
                  case _:
                      # el cursor está encima → lo iluminamos de blanco
                      if 532+80.6*(columna) < m_pos[0] < 524+80.6*(columna+1) and 240+80*fila < m_pos[1] < 240+80.6*(fila+1):
                          self.mostrar_texto(self.pantalla,str(1 +fila*3 + columna),cte.fuente_p1,35,cte.BLANCO,(560+80*columna,259+80*fila))
                      # el cursor no está encima → lo coloreamos de blanco transparente
                      else:
                          self.mostrar_texto(self.pantalla_trans,str(1 +fila*3 + columna),cte.fuente_p1,35,cte.BLANCO_T,(560+80*columna,259+80*fila))
  
  def transicion(self):
      """
      Realiza una transición de opacidad en la pantalla.
      """
      if self.transparencia > 0:
          self.transparencia -= 5
          pg.draw.rect(self.pantalla_trans, (0,0,0,self.transparencia), (0,0,1280, 720))
          self.pantalla.blit(self.pantalla_trans, (0,0))

  def dibujar_elementos(self):
      """
      Dibuja los restantes elementos en la pantalla (botones y puntuación).
      Si el cursor se sitúa sobre un botón, este se iluminará. En caso contrario, permanecerá en reposo.
      """
      # PUNTUACIÓN
      # Simbolo del jugador
      self.mostrar_texto(self.pantalla,self.jugador1.simbolo, cte.fuente_p1, 35, cte.BLANCO,(545, 600))
      self.mostrar_texto(self.pantalla,self.jugador2.simbolo, cte.fuente_p1, 35, cte.BLANCO,(665, 600))
      # Separador :
      self.mostrar_texto(self.pantalla,':', None, 35, cte.BLANCO,(575, 610))
      self.mostrar_texto(self.pantalla,':', None, 35, cte.BLANCO,(695, 610))
      # Cantidad de Puntuación
      self.mostrar_texto(self.pantalla, str(self.jugador1.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(600, 600))
      self.mostrar_texto(self.pantalla, str(self.jugador2.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(720, 600))
      
      # BOTONES EN REPOSO - Transparentes
      # Salir
      pg.draw.rect(self.pantalla_trans, cte.amarillo_t1_T,(50,25,150,55))
      pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(50,25,150,55),2)
      self.mostrar_texto(self.pantalla_trans, 'SALIR', cte.fuente_p1, 20, cte.BLANCO2_T, (100,40))
      # Reiniciar
      pg.draw.rect(self.pantalla_trans, cte.amarillo_t1_T,(1080,25,150,55))
      pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(1080,25,150,55),2)
      self.mostrar_texto(self.pantalla_trans, 'REINICIAR', cte.fuente_p1, 20, cte.BLANCO2_T, (1115,40))      

      # BOTONES ILUMINADOS 
      m_pos = pg.mouse.get_pos()
      # Salir
      if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
          pg.draw.rect(self.pantalla, cte.amarillo_t1,(50,25,150,55))
          pg.draw.rect(self.pantalla, cte.BLANCO,(50,25,150,55),2)
          self.mostrar_texto(self.pantalla, 'SALIR',cte.fuente_p1, 20, cte.BLANCO, (100,40))
      # Reiniciar
      if 1080 < m_pos[0] < 1230 and 25 < m_pos[1] < 80:
          pg.draw.rect(self.pantalla, cte.amarillo_t1,(1080,25,150,55))
          pg.draw.rect(self.pantalla, cte.BLANCO,(1080,25,150,55),2)
          self.mostrar_texto(self.pantalla, 'REINICIAR',cte.fuente_p1, 20, cte.BLANCO, (1115,40))   
