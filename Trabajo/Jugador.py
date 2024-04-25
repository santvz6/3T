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

class Jugador2():
    def __init__(self, pantalla): 

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

                self.signo = True if random.randint(0,1) == 1 else False    # Aleatoriamente se decide hacia que lado 
                if self.rect.y < 720 - self.rect.height:                    # se dirige el jugador al hacer click       
                    self.puntuacion += 1 # cuando el jugador se encuentra en el aire se habilita la puntuación
                
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
            '''
            Requesitos:
            1 º Añadir al archivo.bson self.puntuacion en esta línea de código
            2 º Comprobar si se ha realizado un récord nuevo
            3 º Devolver en una variable la mayor puntuación   
            '''

        # Dibujo del jugador en la pantalla
        self.pantalla.blit(self.image,(self.rect.x,self.rect.y))