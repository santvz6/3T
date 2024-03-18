def victoria_3x5(self):
  # Verificar filas
  for fila in self.tablero:
      for n in range(5):
          filas += str(fila[n])
      filasx2 = fila*2

      if self.simbolo in filasx2:
          return (True, self.simbolo)

  # Verificar columnas
  for columna in self.tablero:
      for n in range(5):
          columnas += str(columna[n])
      columnasx2 = columna*2

      if self.simbolo in columnasx2:
          return (True, self.simbolo)

  # Verificar diagonales
  #Izq - der
  for i in range(5):
      diagonal = ''
      for j in range(5):
          diagonal += str(self.tablero[j][(i+j)%5])
      diagonalx2 = diagonal*2

      if self.simbolo*3 in diagonalx2:
          return (True, self.simbolo)
      
  #Der - izq
  for i in range(5, 0, -1):
      diagonal = ''
      for j in range(5, 0, -1):
          diagonal += str(self.tablero[j-1][-(j-5+i)])
          diagonalx2 = diagonal*2

      if self.simbolo in diagonalx2:
          return (True, self.simbolo)
      
  return (False, None)
