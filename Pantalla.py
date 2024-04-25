import pygame as pg
import sys

# Ficheros
import cte

from Settings.T1_settings import Tablero1
from Settings.T2_settings import Tablero2
from Settings.T3_settings import Tablero3
from Settings.Easter_Egg import EasterEgg

import UI_db.DataBase as db
from UI_db.ui_login import UiLogin


# Pantalla se encargará de establecer cada tipo de escenario y de
# seleccionar mediante update() que escenario cargar


class Pantalla:
    def __init__(self, main):

        # Atributos de instancia
        self.main = main     # Contiene todos los self de main.py

        self.pantalla = self.main.pantalla                  
        self.pantalla_trans = self.main.pantalla_trans      
        self.cambio_pantalla = self.main.juego_inicial    # pantalla actual
                               
        
        self.mini_victorias_2t = []     # guarda aquellas matrices de 3x3 ganadas

        #self.cambio_pantalla = '2t' # pantalla en específico para pruebas

        # Instancias
        self.t1_set = Tablero1(self.pantalla, self.pantalla_trans)
        self.t2_set = Tablero2(self.pantalla, self.pantalla_trans)
        self.t3_set = Tablero3(self.pantalla, self.pantalla_trans)
        self.easter_set = EasterEgg(self.pantalla, self.pantalla_trans)
        


    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: # El usuario presiona la X roja de salir
                db.set_inactivo()   
                sys.exit()

        ################## EVENTO (PULSAR ALGO) ################## 
            if self.cambio_pantalla == '1t':
                # CLICK IZQUIERDO
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  
                    m_pos = pg.mouse.get_pos()

                    # Coordenadas Número Tablero
                    if not self.t1_set.victoria_1t(self.t1_set.tablero)[0]:                     
                        self.t1_set.actualizar_1t_mouse()
                        
                    # Coordenadas Botón Salir
                    if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
                        self.cambio_pantalla = 'menu'

                    # Coordenadas Botón Reiniciar
                    if 1080 < m_pos[0] < 1230 and 25 < m_pos[1] < 80:
                        self.t1_set.reinicio_1t()

                # KEYDOWN DE UNA TECLA
                if event.type == pg.KEYDOWN: 

                    # Números del 1 al 9
                    if pg.K_1 <= event.key <= pg.K_9:
                        self.t1_set.update()
                        self.t1_set.actualizar_1t_teclas(int(event.unicode)) # event.unicode → nos dice que número se presionó


            elif self.cambio_pantalla == '2t':

                # CLICK DERECHO
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  
                    m_pos = pg.mouse.get_pos()

                    # Coordenadas Número Tablero
                    if not self.t2_set.victoria_2t(self.mini_victorias_2t)[0]:
                        self.t2_set.actualizar_2t_mouse(self.mini_victorias_2t)
                        self.mini_victorias_2t = self.t2_set.get_mini_victorias()
                        
                         
                        

                    # Coordenadas Botón Salir
                    if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
                        self.cambio_pantalla = 'menu'

                    # Coordenadas Botón Reiniciar
                    if 1045 < m_pos[0] < 1195 and 25 < m_pos[1] < 80:
                        self.t2_set.reinicio_2t()

                # KEYDOWN DE UNA TECLA
                if event.type == pg.KEYDOWN: 

                    # Números del 1 al 9
                    if pg.K_1 <= event.key <= pg.K_9:
                        self.t2_set.update(self.mini_victorias_2t)
                        self.t2_set.actualizar_2t_teclas(int(event.unicode), self.mini_victorias_2t) # event.unicode → nos dice que número se presionó
                        self.mini_victorias_2t = self.t2_set.get_mini_victorias()


            elif self.cambio_pantalla == '3t':
                # CLICK IZQUIERDO
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    print(1)
                    self.t3_set.dibujar_3t([])

            elif self.cambio_pantalla == 'easter_egg':
                if event.type == pg.MOUSEBUTTONDOWN and event.button==1: # event.button == 1 : Click derecho
                    m_pos = pg.mouse.get_pos() # Nos devuelve la pos del ratón cuando se hace MOUSEBOTTONDOWN
                    self.easter_set.update(m_pos)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.cambio_pantalla = 'menu'
            
        ########################################################################


        ################## BUCLE CONSTANTE ##################

        if self.cambio_pantalla == 'menu':
            
            # En un foro de stack overflow podemos ver como ocultar una 
            # pantalla en pygame sin necesidad de hacer: pygame.quit()
            # https://stackoverflow.com/questions/10466590/hiding-pygame-display    
                    
            self.pantalla = pg.display.set_mode((1280,720), flags=pg.HIDDEN)    # ocultamos el display de pygame
            
            self.main.ui.menu.deiconify()   # volvemos a mostrar el display de customtkinter
            self.main.ui.mainloop()         # llamamos al mainloop (bucle)
        
            # Una vez cerrado → ui.mainloop() esta parte del código se ejecutará
            self.pantalla = pg.display.set_mode((1280,720), flags=pg.SHOWN)     # mostramos el display de pygame


        ################## T1 ##################
        elif self.cambio_pantalla == '1t':
            
            if not self.t1_set.victoria_1t(self.t1_set.tablero)[0] and self.t1_set.return_num_mov() < 9:   # NO hay victoria
                self.t1_set.update()    # update está creado en T1_settings → t1_set (update es la forma correcta para ejcutar T1)

            else:                                                                       # SÍ hay victoria
                # Si gana el J1, lo gaurdamos en la DB
                if self.t1_set.jugador1.simbolo == self.t1_set.victoria_1t(self.t1_set.tablero)[1]:
                    db.puntuar_db(db.return_activo()[0],'T1',1)     # db: permanente
                    self.t1_set.jugador1.puntuacion += 1            # sesión: temporal

                # Si gana el J2, se guarda en la sesión    
                elif self.t1_set.jugador2.simbolo == self.t1_set.victoria_1t(self.t1_set.tablero)[1]:
                    self.t1_set.jugador2.puntuacion += 1 # sesión: temporal

                
                # else: Si hay empate no ocurre nada

                # Reinicio de ajustes
                self.t1_set.reinicio_1t()
                self.cambio_pantalla = 'refresh_1t' # nos vemos a una pantalla de carga
              
        # Pantalla de carga T1
        elif self.cambio_pantalla == 'refresh_1t':        
            self.t1_set.update()                # seguimos mostrando el juego durante la pantalla de carga
            self.t1_set.transicion()            # bajamos la opacidad para darle un efecto desvanecedor

            if self.t1_set.transparencia < 1:   # cuando la opacidad llega al mínimo
                self.cambio_pantalla = '1t'     # se habilita poder jugar de nuevo

        ################## 2T ##################
        elif self.cambio_pantalla == '2t':
           
            if not self.t2_set.victoria_2t(self.mini_victorias_2t)[0]: # falta condición num mov 81 y empate ?

                self.mini_victorias_2t = self.t2_set.get_mini_victorias()   # comprobamos el estado actual del tablero
                                                                        # para añdir nuevas mini_victorias
                
                self.t2_set.update(self.mini_victorias_2t)      # como argumento le damos una lista de tuplas
                                                                # cada elemento de la lista es una matriz ganada
                                                                # la tupla corresponde a la fila y la columna

            else:
                if self.t2_set.jugador1.simbolo == self.t2_set.victoria_2t(self.mini_victorias_2t)[1]:
                    db.puntuar_db(db.return_activo()[0],'T2',1) 
                    self.t2_set.jugador1.puntuacion += 1 
                elif self.t2_set.jugador2.simbolo == self.t2_set.victoria_2t(self.mini_victorias_2t)[1]:
                    self.t2_set.jugador2.puntuacion += 1
                
                # Reinicio de ajustes
                self.t2_set.reinicio_2t()
                self.mini_victorias_2t = []

                self.cambio_pantalla = 'refresh_2t' # nos vemos a una pantalla de carga

        # Pantalla de carga T2
        elif self.cambio_pantalla == 'refresh_2t':     
            self.t2_set.update(self.mini_victorias_2t)  # seguimos mostrando el juego durante la pantalla de carga
            self.t1_set.transicion()                    # Reutilizamos la transición de T1
            
            if self.t1_set.transparencia < 1:           # cuando la opacidad llega al mínimo
                self.cambio_pantalla = '2t'             # se habilita poder jugar de nuevo
        
        ################## 3T ##################
        elif self.cambio_pantalla == '3t':
            self.t3_set.update()


        elif self.cambio_pantalla == 'easter_egg':
            self.easter_set.update(None)
            
        pg.display.update()
