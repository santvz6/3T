import pygame as pg
from Jugador import Jugador
import cte

class Tablero1:
  def __init__(self, pantalla):

    # Creación del tablero
    self.tablero = [[str((n+1)+(m*3)) for n in range(3)] for m in range(3)]
    #print(self.tablero)

    # Instancias iniciales
    self.jugador1 = Jugador('Jug1','X', 0)
    self.jugador2 = Jugador('Jug2', '0', 0)

    # Atributos de instancia
    self.pantalla = pantalla 
    self.actual = self.jugador1 # Primer movimiento

    

########################### LÓGICA DEL JUEGO ORIENTADA A PYTHON VANILLA ###########################

  # Cambio de turno (En un futuro crear un super.turno() para reutilizarlo)
  def turno(self):
    self.actual = self.jugador1 if self.jugador2 == self.actual else self.jugador2

  def victoria_1t(self):
    # Verificar filas
    for fila in self.tablero:
      if fila[0] == fila[1] == fila[2]:
        return True

    # Verificar columnas
    for columna in range(3):
      if self.tablero[0][columna] == self.tablero[1][columna] == self.tablero[2][columna]:
        return True

    # Verificar diagonales
    if self.tablero[0][0] == self.tablero[1][
        1] == self.tablero[2][2]:
      return True
    if self.tablero[0][2] == self.tablero[1][
        1] == self.tablero[2][0]:
      return True

    return False




########################### LÓGICA DEL JUEGO ORIENTADA A PYGAME ###########################
  def mostrar_texto(self, texto, fuente, tamaño, color, posicion):
    # Crear un objeto de texto
    font = pg.font.Font(fuente, tamaño)
    text_surface = font.render(texto, True, color)

    # Obtener el rectángulo del texto y configurar la posición
    text_rect = text_surface.get_rect()
    text_rect.topleft = posicion

    # Dibujar el texto en la pantalla
    self.pantalla.blit(text_surface, text_rect)

  def dbujar_1t(self):
    self.fondo_1t = pg.image.load('T1/Imagenes/1t.png')
    self.fuente_p1 = ('T1/Fuentes/P1.ttf')
    self.pantalla.blit(self.fondo_1t,(0,0))
    for y in range(3):
      for x in range(3):
        self.mostrar_texto(self.tablero[y][x],self.fuente_p1,35,cte.BLANCO,(560+80*x,259+80*y))

  # Actualización el tablero cuando se hace click
  def actualizar_1t(self):
    m_pos = pg.mouse.get_pos()
    for y in range(3):
      for x in range(3):
        if 532+80.6*(x) < m_pos[0] < 524+80.6*(x+1) and 240+80*y < m_pos[1] < 240+80.6*(y+1):
          # Validación casilla sin jugar
          if self.tablero[y][x] in ['1','2','3','4','5','6','7','8','9']:
            self.tablero[y][x] = self.actual.simbolo
            self.turno()
