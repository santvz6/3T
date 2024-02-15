import random
import numpy

class Tablero1:
    def __init__(self):
        self.tablero = [[' ' for _ in range(3)] for _ in range(3)]
        # print(self.tablero)

    def dibujar(self):
        for fila in range(len(self.tablero)):
            for columna in range(len(self.tablero)):
                print(f'| {fila * 3 + columna + 1} |', end=' ')
            print()

    def actualizar(self, filas, columnas):
        self.filas = filas
        self.columas = columnas


class Jugador:
    def __init__(self, nombre, simbolo):
        self.nombre = nombre
        self.simbolo = simbolo


class Juego:
    def __init__(self):
        self.jugador1 = Jugador('Jug1', 'X')
        self.jugador2 = Jugador('Jug2', 'O')
        # print(self.jugador1.nombre) # mención a cualquier jugador
        self.tablero = Tablero1()

    def turno(self):
        self.actual = self.jugador1 if self.jugador2 == self.actual else self.jugador1

    def comprobar(self):
        # Verificar filas
        for fila in self.tablero:
            if fila[0] == fila[1] == fila[2] != ' ':
                return True

        # Verificar columnas
        for columna in range(3):
            if self.tablero[0][columna] == self.tablero[1][columna] == self.tablero[2][columna] != ' ':
                return True

        # Verificar diagonales
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != ' ':
            return True
        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != ' ':
            return True

        return False

    def jugar(self):
        # filas / columnas -> usadas en def actualizar():
        if self.actual == self.jugador1:
            self.fila = int(input('Ingrese fila: '))
            self.columna = int(input('Ingrese columna: '))
            ### ... ###
            self.turno()
        pass


tablero = Tablero1()
juego = Juego()

tablero.dibujar()
