""" 
Este fichero contiene la creación de la clase Jugador y Jugador2, ambas clases establecen atributos necesarios en la ejecución de los juegos.

También utilizamos las librerías incorporadas en Python:
* pickle: utilizado para crear/escribir/leer archivos .pickle
* pygame: utilizada para la creación del display para mostrar todos los correspondientes elementos
* cte: utilizada para acceder a valores constantes en todo el código
* UI_db.DataBase:  contiene el código encargado de administrar la tabla de usuarios.
"""
import pickle
import pygame as pg
import cte
import random
from UI_db.DataBase import db_principal as db


class Jugador:
  """
  Clase encargada de establecer los atributos principales del
  Jugador en los 4 principales juegos(T1, T2, T3, M35)
  """
  def __init__(self, nombre:str, simbolo:str, puntuacion:int, color: tuple|str):
    """
    Cada jugador se instancia con los siguientes parámetros   
    
    Parámetros
    ----------
    nombre: str
        Representa el nombre de cada jugador instanciado
    simbolo: str
        Representa el símbolo de la ficha del jugador. El límite de longitud del símbolo es 2 (np.dtype('U2'))
    puntuacion: int
        Representa la puntuación temporal (puntuación de la sesión actual)
    color: tuple|str
        Representa el color de la ficha del jugador. Puede ser representado en hexadecimal, RGB o RGBA

    """
    self.nombre = nombre
    self.simbolo = simbolo
    self.puntuacion = puntuacion
    self.color = color


# Jugador dedicado al Easter Egg
class Jugador2:
    """
    Clase encargada de establecer los atributos principales del Easter_Egg

    Atributos
    --------
    activo : tupla
        Devuelve el jugador activo
    puntuacion : int
        Guarda el score del jugador
    image : pygame.image
        Cuadrado del jugador
    rect : pygame.Rect
        Imagen del jugador, físicas del jugador (colisiones)
    velocidad_y : int
        Indica la velocidad a la que se mueve la imagen
    signo : bool
        Indica la direccion a donde se mueve la imagen

    Métodos
    -------
    __init__(self)
           Inicializa la clase con los atributos especificados
    update(self, saltar)
        Actualiza la imagen del jugador en cada iteración del bucle

    """
    def __init__(self):
        self.activo = db.returnActivo()[0]

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

        with open('easter_egg_score.pkl', 'rb') as data_reader:
            data = pickle.load(data_reader)
            self.personal_hs = data['PERSONAL_HIGH_SCORES'][self.activo]  # Récord personal
            self.global_hs = data['GLOBAL_HIGH_SCORE']                    # Récord global

    def update(self, saltar: bool|None):
        """
        Actualiza la imagen del jugador en cada iteración del bucle

        Parámetros
        ---------
        saltar : bool
            Indica cuando se hace click en la imagen del jugador, y las coordenadas del sitio donde se ha hecho click
        """
        # Físicas del jugador
      
        """
        Conceptos para diseñar las físicas del jugador:

        1. self.rect.x += valor ; Al estar dentro de un bucle while el valor actúa como velocidad consante del objeto (MRU)
                                ; A la posición se le suma todo el rato un valor constante

        2. self.rect.x += self.velocidad_x  ; Como el valor de velocidad_x aumenta en cada iteración, este actúa como aceleración (MRUA)
                                            ; A la posición se le suma un dato que varía con el tiempo
        """
        if saltar: # Tecla de salto (right_click)
            if self.rect.topleft[0] < saltar[0] < self.rect.topleft[0] + self.rect.width and \
                self.rect.topleft[1] < saltar[1] < self.rect.topleft[1] + self.rect.width: # Click en el rectángulo del jugador
                
                self.velocidad_y = -15
                self.puntuacion += 1

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

        # LÍMETES
        # Paredes
        if self.rect.x < 0:
            self.signo = True
        elif self.rect.x > 1280 - self.rect.width:
            self.signo = False
        # Suelo
        if self.rect.y > 720 - self.rect.height:
            self.rect.y = 720 - self.rect.height
            self.puntuacion = 0  # Si el jugador cae al suelo, se pierde el streak
        # Techo
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocidad_y = 0
