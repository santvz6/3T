""" Jugador.py

Este fichero contiene las clases Jugador y Jugador2, las cuales son utilizadas tanto para los tres en raya como para
el Easter Egg (contienen los datos de los jugadores, y en el caso de Jugador2, las físicas del Easter Egg).

El fichero trabaja con la tabla de usuarios ubicada en Ui_db.DataBase.py, denominada como db_principal para llevar un
recuento de las puntuaciones en el Easter Egg. También hace uso del módulo cte, en donde se encuentran valores
constantes como los de los colores.

Para utilizar el código, es necesario tener instaladas las librerías pygame y pickle (así como random, que viene por
defecto instalada en python).
"""

class Jugador:
    """
    Contiene los atributos del jugador de los tres en raya.

    Atributos
    ---------
    nombre : str
        Nombre del jugador.
    simbolo : str
        Símbolo del jugador.
    puntuacion : int
        Puntuación del jugador.
    color : tuple
        Color del jugador.

    Métodos
    -------
    __init__(self, nombre, simbolo,  puntuacion, color)
        Crea la instancia de la clase con los atributos especificados.
    """
    def __init__(self, nombre, simbolo, puntuacion, color):
        self.nombre = nombre
        self.simbolo = simbolo
        self.puntuacion = puntuacion
        self.color = color


# Jugador dedicado al Easter Egg

import pygame as pg
import cte
import random
import pickle
from UI_db.DataBase import db_principal as db

class Jugador2():
    """
    Crea la ventana del Easter Egg y reúne todos los atributos del jugador en el Easter Egg, así como las físicas.

    Atributos
    ---------
    activo : str
        Nombre del jugador activo
    pantalla : Pantalla
        La ventana del Easter Egg.
    puntuacion : int
        Puntuación del jugador.

    Métodos
    -------
    __init__(self, pantalla)
        Crea la instancia de la clase con los atributos especificados.
    update(self, saltar:tuple)
        Se utiliza para crear el bucle de juego del Easter Egg.
    """

    def __init__(self, pantalla):
        """
        Crea la instancia de la clase con los parámetros especificados. Aquí se atribuyen todos los assets de la
        ventana del Easter Egg a variables de la instancia.

        Parámetros
        ----------
        pantalla : Pantalla
            La ventana del Easter Egg

        Variables
        ---------
        self.activo : str
            Nombre del jugador activo.
        self.puntuacion : int
            Puntuación actual.
        self.image : pg.transform.scale
            La imagen del jugador.
        self.rect : pygame.Rect
            Rectángulo con colisión de la imagen del jugador.
        self.rect.center : tuple
            Posición del centro del rectángulo del jugador.
        self.velocidad_y : int
            Velocidad base en el eje Y del jugador.
        self.signo : int
            Valor aleatorio (0 o 1) mediante el cual se decide si el jugador va hacia un lado o hacia otro.
        """
        self.activo = db.returnActivo()[0]
        self.pantalla = pantalla
        self.puntuacion = 0

        # Dibujo del jugador
        self.image = pg.transform.scale(pg.image.load('./Imagenes/EG/prueba.png').convert(),(80,80))
        self.image.blit(cte.easter_player,(0,0),pg.Rect(0, 0, 80, 80)) 
        # Posición del jugador
        self.rect = self.image.get_rect()           # Asignamos a rect el valor del tamaño rectángulo de la Surface/Imagen (self.image)
        self.rect.center = (1280/2, 720-self.rect.height)
        # Física del jugador
        self.velocidad_y = 0 # definimos la variable velocidad_y
        self.signo = True if random.randint(0,1) == 1 else False

    def update(self, saltar:tuple):
        """
        Método que actualiza la posición del jugador y define las físicas del jugador.

        Conceptos para diseñar las físicas del jugador:

        1. self.rect.x += valor ; Al estar dentro de un bucle while el valor actúa como velocidad consante del objeto (MRU)
                                ; A la posición se le suma todo el rato un valor constante

        2. self.rect.x += self.velocidad_x  ; Como el valor de velocidad_x aumenta en cada iteración, este actúa como aceleración (MRUA)
                                            ; A la posición se le suma un dato que varía con el tiempo

        Además de definir las físicas (controla la posición en x e y del jugador), también lleva un recuento de las
        puntuaciones más altas de los jugadores cada vez que se hace click.


        Parámetros
        ----------
        saltar : tuple
            Indica si se ha hecho click sobre el jugador en el momento de llamar al método.
        """

        if saltar: # Tecla de salto
            if self.rect.topleft[0] < saltar[0] < self.rect.topleft[0] + self.rect.width and \
                self.rect.topleft[1] < saltar[1] < self.rect.topleft[1] + self.rect.width: # Click en el rectángulo del jugador
                self.velocidad_y = -15
                self.puntuacion += 1

                self.signo = random.randint(0,1)    # Aleatoriamente se decide hacia que lado
                                                          # se dirige el jugador al hacer click

        if self.signo:      # Movimiento elegido hacia la derecha
            self.rect.x += 7
        else:               # Movimiento elegido hacia la izquierda
            self.rect.x -= 7

        ### ↓ Bucle constante ↓ ###

        # Físicas del jugador
        self.velocidad_y += 0.5         
        self.rect.y += self.velocidad_y 
        # Dibujo del jugador
        self.image = pg.transform.scale(pg.image.load('./Imagenes/EG/prueba.png').convert(),(80,80))
        self.image.blit(cte.easter_player,(0,0),pg.Rect(0, 0, 80, 80))
        # Márgenes del jugador
        # - Eje X 
        if self.rect.x < 0 - self.rect.width:
            self.rect.x = 1280
        elif self.rect.x > 1280:
            self.rect.x = 0 - self.rect.width
        # - Eje Y
        if self.rect.y > 720 - self.rect.height:
            self.rect.y = 720 - self.rect.height
            self.puntuacion = 0  # Si el jugador cae al suelo, se pierde el streak

        # Obtenemos los scores
        with open('easter_egg_score.pkl', 'rb') as data_reader:
            data = pickle.load(data_reader)

        # Update del personal high score
        if data['PERSONAL_HIGH_SCORES'][self.activo] < self.puntuacion:
            data['PERSONAL_HIGH_SCORES'][self.activo] = self.puntuacion

        # Update del high score global
        if data['GLOBAL_HIGH_SCORE'] < self.puntuacion:
            data['GLOBAL_HIGH_SCORE'] = self.puntuacion

        self.personal_hs = data['PERSONAL_HIGH_SCORES'][self.activo]  # Récord personal
        self.global_hs = data['GLOBAL_HIGH_SCORE']                    # Récord global


        with open('easter_egg_score.pkl', 'wb') as data_writer:  # Update de los datos
            pickle.dump(data, data_writer)


        # Dibujo del jugador en la pantalla
        self.pantalla.blit(self.image,(self.rect.x,self.rect.y))