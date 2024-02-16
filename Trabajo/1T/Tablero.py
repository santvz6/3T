class Tablero1:

  def __init__(self):
    self.tablero = [['-' for _ in range(3)] for _ in range(3)]
    # print(self.tablero)

  def dibujar(self):
    for fila in range(len(self.tablero)):
      for columna in range(len(self.tablero)):
        if self.tablero[fila][columna] == '-':
          self.tablero[fila][columna] = (f'| {fila * 3 + columna + 1} |')
          print(self.tablero[fila][columna], end=' ')
        else:
          print(self.tablero[fila][columna], end=' ')
      print()

  def actualizar(self, fila, columna, simbolo):
    self.tablero[fila][columna] = (f'| {simbolo} |')
