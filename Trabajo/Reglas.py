from Jugador import Jugador
from Tablero import Tablero1


class Reglas:

  def __init__(self, nombre):
    self.nombre = nombre

    # Ajustes iniciales
    self.jugador1 = Jugador('Jug1',
                            'X', 0)  # guardaremos los jugadores en en ajustes
    self.jugador2 = Jugador('Jug2', '0', 0)
    self.tablero = Tablero1()
    self.actual = self.jugador1

  def datos(self):
    self.pos = input('Posición: ') 
  
    while self.pos > '9' or self.pos < '1' or not self.pos.isdigit():
      print('Posición no válida.')
      self.pos = input('Posición: ')

    # Una vez se introduce un número válido
    self.pos = int(self.pos)

    
    # Transformación a filas/columnas
    self.fila = (self.pos - 1) // 3
    self.columna = (self.pos - 1) % 3

    return self.fila, self.columna

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
  

# Lo instanciamos fuera para poder reutilizar 
# la misma instancia en más ficheros
reglas = Reglas('Settings1')
