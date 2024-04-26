# Jugador dedicado a los juegos de mesa

class Jugador:
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
import UI_db.DataBase as db

class Jugador2():
    def __init__(self, pantalla): 
        self.activo = db.return_activo()[0]

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
        #print(self.puntuacion)
        # Físicas del jugador
        '''
        Conceptos para diseñar las físicas del jugador:

        1. self.rect.x += valor ; Al estar dentro de un bucle while el valor actúa como velocidad consante del objeto (MRU)
                                ; A la posición se le suma todo el rato un valor constante

        2. self.rect.x += self.velocidad_x  ; Como el valor de velocidad_x aumenta en cada iteración, este actúa como aceleración (MRUA)
                                            ; A la posición se le suma un dato que varía con el tiempo
        '''
        if saltar: # Tecla de salto (right_click)
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
