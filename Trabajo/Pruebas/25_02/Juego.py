from Reglas import reglas


class Juego:
    def __init__(self):
        # Instancias
        self.reglas = reglas
        self.cont = 0
        
    def jugar(self):
        self.reglas.tablero.dibujar()

        # Introducción de datos
        #self.datos = self.reglas.datos()
        #self.fila = self.datos[0]
        #self.columna = self.datos[1]

        # SIN INPUTS
        self.fila = 1
        self.columna = 1

        # Comprobación jugada ganadora
        if not self.reglas.victoria(self.fila, self.columna) and self.cont < 9:
            # Comprobación validez
            if not self.reglas.valido(self.fila, self.columna):
                print('Jugada no válida')

                # Introducción de datos
                #self.datos = self.reglas.datos()
                #self.fila = self.datos[0]
                #self.columna = self.datos[1]

            # Movimiento Válido
            else:
                # Actualizar el tablero con el movimiento del jugador
                self.reglas.tablero.actualizar(self.fila, self.columna,
                                               self.reglas.actual.simbolo)
                self.reglas.tablero.dibujar()

                # Cambio de turno
                self.reglas.turno()

                # Contador de movimiento
                self.cont += 1
                
                #print('TABLERO: ', self.reglas.tablero.tablero)

                #if not self.reglas.victoria(self.fila, self.columna):
                    # Introducción de datos
                    #if self.cont < 9:
                        #self.datos = self.reglas.datos()
                        #self.fila = self.datos[0]
                        #self.columna = self.datos[1]

        # Una vez finalizado el bucle

        self.reglas.turno()  # Actual toma el valor del Ganador
        # self.reglas.tablero.dibujar() # Tablero final

        # Si se produce una victoria
        if self.reglas.victoria(self.fila, self.columna):
            print(f'Ganó {self.reglas.actual.nombre}')  # actual: es el ganador
            self.reglas.actual.puntuacion += 1

        # Empate
        else:
            self.reglas.tablero.dibujar()
            print('Empate')

        print(
            f'Jugador1: {self.reglas.jugador1.puntuacion} - {self.reglas.jugador2.puntuacion} :Jugador2')


#juego = Juego()
#juego.jugar()
