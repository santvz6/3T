def victoria_3x5(self):
  # Verificar filas
    for fila in self.tablero:
        for n in range(5):
            filas += str(fila[n])

        if self.simbolo in filas:
            return (True, self.simbolo)

  # Verificar columnas
    for columna in self.tablero:
        for n in range(5):
            columnas += str(columna[n])

        if self.simbolo in columnas:
            return (True, self.simbolo)

  # Verificar diagonales
  #Izq - der
    for i in range(5):
        diagonal = ''
        if i == 0:
        ini = 0
        f = 5

        if i == 1:
        ini = 0
        f = 4

        if i == 2:
        ini = 0
        f = 3

        if i == 3:
        ini = 2
        f = 5

        if i == 4:
        ini = 1
        f = 5

        for j in range(ini, f, 1):
            diagonal += str(self.tablero[j][(i+j)%5]) + ' '      
        
        if self.simbolo*3 in diagonal:
            return (True, self.simbolo)
    
  #Der - izq
    for i in range(5):
        diagonal2 = ''
        if i == 0:
        ini = 5
        f = 0

        if i == 1:
        ini = 4
        f = 0

        if i == 2:
        ini = 3
        f = 0

        if i == 3:
        ini = 5
        f = 2

        if i == 4:
        ini = 5
        f = 1

        for j in range(ini, f, -1):
            diagonal2 += str(self.tablero[j-1][-(j-5+i)]) + ' '
  
        if self.simbolo*3 in diagonal2:
            return (True, self.simbolo)
    
    return (False, None)
