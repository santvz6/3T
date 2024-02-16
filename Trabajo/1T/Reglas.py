from Jugador import Jugador
from Tablero import Tablero1


class Reglas:

  def __init__(self, nombre):
    self.nombre = nombre

    # Ajustes iniciales
    self.jugador1 = Jugador('Jug1',
                            'X')  # guardaremos los jugadores en en ajustes
    self.jugador2 = Jugador('Jug2', 'O')
    self.tablero = Tablero1()
    self.actual = self.jugador1

  def datos(self):

    self.fila = int(input(f'Jugador {self.actual.nombre} Ingrese fila: '))
    self.columna = int(
        input(f'Jugador {self.actual.nombre} Ingrese columna: '))

    while self.fila > len(self.tablero.tablero) or self.columna > len(
        self.tablero.tablero):
      print('\n Jugada no válida. \n')
      self.fila = int(input(f'Jugador {self.actual.nombre} Ingrese fila: '))
      self.columna = int(
          input(f'Jugador {self.actual.nombre} Ingrese columna: '))

    return self.fila - 1, self.columna - 1

  def turno(self):
    self.actual = self.jugador1 if self.jugador2 == self.actual else self.jugador2

  def valido(self, fila, columna):
    self.continuar = True

    if self.tablero.tablero[fila][columna] == (f'| {self.jugador1.simbolo} |') \
    or self.tablero.tablero[fila][columna] == (f'| {self.jugador2.simbolo} |'):
      self.continuar = False

    return self.continuar

  def victoria(self, fila, columna):
    # Verificar filas
    for fila in self.tablero.tablero:
      if fila[0] == fila[1] == fila[2] != ' ':
        return True

    # Verificar columnas
    for columna in range(3):
      if self.tablero.tablero[0][columna] == self.tablero.tablero[1][
          columna] == self.tablero.tablero[2][columna] != ' ':
        return True

    # Verificar diagonales
    if self.tablero.tablero[0][0] == self.tablero.tablero[1][
        1] == self.tablero.tablero[2][2] != ' ':
      return True
    if self.tablero.tablero[0][2] == self.tablero.tablero[1][
        1] == self.tablero.tablero[2][0] != ' ':
      return True

    return False
