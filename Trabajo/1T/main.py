from Reglas import Reglas

class Juego:
  def __init__(self):
    # Instancias
    self.reglas = Reglas('Setting1')

  def jugar(self):
    self.reglas.tablero.dibujar()

    # Introducción de datos
    self.datos = self.reglas.datos()
    self.fila = self.datos[0]
    self.columna = self.datos[1]

    # Comprobación jugada ganadora
    while not self.reglas.victoria(self.fila, self.columna):

      # Comprobación validez
      if not self.reglas.valido(self.fila, self.columna):
        print('Jugada no válida')

        # Introducción de datos
        self.datos = self.reglas.datos()
        self.fila = self.datos[0]
        self.columna = self.datos[1]

      else:
        # Actualizar el tablero con el movimiento del jugador
        self.reglas.tablero.actualizar(self.fila, self.columna,
                                       self.reglas.actual.simbolo)
        self.reglas.tablero.dibujar()

        # Cambio de turno
        self.reglas.turno()

        # Introducción de datos
        self.datos = self.reglas.datos()
        self.fila = self.datos[0]
        self.columna = self.datos[1]


juego = Juego()
juego.jugar()
