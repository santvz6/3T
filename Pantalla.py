import pygame as pg
import sys

# Ficheros
import cte

from Settings.T1_settings import Tablero1
from Settings.T2_settings import Tablero2
from Settings.T3_settings import Tablero3
from Settings.Easter_Egg import EasterEgg
from Settings.M35_settings import M35

from UI_db.DataBase import db_principal as db

class Pantalla:
    """
    La clase 'Pantalla' se encarga de establecer cada tipo de escenario haciendo uso de 'self.cambio_pantalla'.
    Mediante el método 'update()' se establecerá el escenario de la pantalla.
    """

    def __init__(self, pantalla, pantalla_transparente, juego_inicial:str, ui):
        """
        En el constructor de la clase 'Pantalla' se inicializan varios atributos y 
        se crean las instancias de todos los ajustes de cada juego creado.
        
        Parámetros:
        pantalla: Pantalla principal.
        pantalla_transparente: Pantalla de transición.
        ui: Representa la interfaz CTk.
        """

        # Parámetros - Atributos
        self.ui = ui                                    # Representa la interfaz CTk
        self.pantalla = pantalla                        # Pantalla principal
        self.pantalla_trans = pantalla_transparente     # Pantalla de transición
        self.juego_inicial = juego_inicial
        self.cambio_pantalla = self.juego_inicial       # Pantalla actual
                               
        # Instancias de los ajustes de cada juego
        self.t1_set = Tablero1(self.pantalla, self.pantalla_trans)  # Instancia de la clase 'Tablero1'
        self.t2_set = Tablero2(self.pantalla, self.pantalla_trans)  # Instancia de la clase 'Tablero2'
        self.t3_set = Tablero3(self.pantalla, self.pantalla_trans)  # Instancia de la clase 'Tablero3'
        self.easter_set = EasterEgg(self.pantalla, self.pantalla_trans)  # Instancia de la clase 'EasterEgg'
        self.m35_set = M35(self.pantalla, self.pantalla_trans)  # Instancia de la clase 'M35'

        # Atributos
        self.tipo_transicion = ''

    def update(self):
        """
        El método update() es utilizado en el método run() del fichero main.py. Por tanto este método está dentro de nuestro
        bucle de juego. Aquí se controlan todas las interacciones que el usuario realiza mediante el uso de pg.event.get().
        Además, gracias al valor de 'self.cambio_pantalla' podremos seleccionar cual de todas las pantalla mostrar.
        """

        for event in pg.event.get():

            #Evento de tipo Salir
            if event.type == pg.QUIT: 
                db.setInactivo()   
                sys.exit()

# *EVENTO* #######################        1T        ###################################
            if self.cambio_pantalla == '1t':

                #Evento de tipo Click Izquierdo
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  
                    m_pos = pg.mouse.get_pos()

                    # JUGAR CASILLA
                    if not self.t1_set.victoria_1t(self.t1_set.tablero)[0] \
                          and self.t1_set.num_movimientos < 9:                     
                        self.t1_set.jugar_casilla(False)
                        
                    # BOTÓN SALIR
                    if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
                        self.cambio_pantalla = 'menu'

                    # BOTÓN REINICIAR
                    if 1080 < m_pos[0] < 1230 and 25 < m_pos[1] < 80:
                        self.t1_set.reinicio_1t()

                #Evento tipo PresionarTecla
                if event.type == pg.KEYDOWN: 

                    # JUGAR CASILLA
                    if pg.K_1 <= event.key <= pg.K_9:
                        self.t1_set.update()
                        self.t1_set.jugar_casilla(int(event.unicode)) # event.unicode → nos dice que número se presionó

# *EVENTO* #######################        2T        ###################################
            elif self.cambio_pantalla == '2t':

                #Evento de tipo Click Izquierdo
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  
                    m_pos = pg.mouse.get_pos()

                    # JUGAR CASILLA
                    if not self.t2_set.victoria_2t()[0] and self.t2_set.numero_movimientos < 81:
                        self.t2_set.jugar_casilla(False)
                        self.t2_set.mini_victorias = self.t2_set.get_mini_victorias()
                        
                    # BOTÓN SALIR
                    if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
                        self.cambio_pantalla = 'menu'

                    # BOTÓN REINICIAR
                    if 1045 < m_pos[0] < 1195 and 25 < m_pos[1] < 80:
                        self.t2_set.reinicio_2t()

                #Evento tipo PresionarTecla
                if event.type == pg.KEYDOWN: 

                    # JUGAR CASILLA
                    if pg.K_1 <= event.key <= pg.K_9:
                        self.t2_set.update()
                        self.t2_set.jugar_casilla(int(event.unicode)) # event.unicode → nos dice que número se presionó
                        self.t2_set.mini_victorias = self.t2_set.get_mini_victorias()

# *EVENTO* #######################        3T        ###################################
            elif self.cambio_pantalla == '3t':
                # CLICK IZQUIERDO
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.t3_set.victoria_3t()[0]:
                        self.t3_set.actualizar_3t_mouse()
                        self.pantalla_trans.fill((0,0,0,0))
                        self.t3_set.dibujar_3t()


            elif self.cambio_pantalla == 'easter_egg':
                if event.type == pg.MOUSEBUTTONDOWN and event.button==1: # event.button == 1 : Click derecho
                    m_pos = pg.mouse.get_pos() # Nos devuelve la pos del ratón cuando se hace MOUSEBOTTONDOWN
                    self.easter_set.update(m_pos)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.cambio_pantalla = 'menu'

# *EVENTO* #######################        M35        ###################################            
            elif self.cambio_pantalla == 'm35':

                #Evento tipo Click Izquierdo
                if event.type == pg.MOUSEBUTTONDOWN: # and event.button == 1:  
                    m_pos = pg.mouse.get_pos()

                    # JUGAR CASILLA
                    if not self.m35_set.victoria_m35()[0]:                     
                        self.m35_set.actualizar_m35_mouse()
                        
                    # BOTÓN SALIR
                    if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
                        self.cambio_pantalla = 'menu'

                    # BOTÓN REINICIAR
                    if 1080 < m_pos[0] < 1230 and 25 < m_pos[1] < 80:
                        self.m35_set.reinicio_m35()


# *BUCLE* #######################        MENÚ        ###################################
        if self.cambio_pantalla == 'menu':
            
            # En un foro de stack overflow podemos ver como ocultar una 
            # pantalla en pygame sin necesidad de hacer: pygame.quit()
            # https://stackoverflow.com/questions/10466590/hiding-pygame-display    
                    
            self.pantalla = pg.display.set_mode((1280,720), flags=pg.HIDDEN)    # ocultamos el display de pygame
            
            self.ui.menu.deiconify()   # volvemos a mostrar el display de customtkinter
            self.ui.mainloop()         # llamamos al mainloop (bucle)
        
            # Una vez cerrado → ui.mainloop() esta parte del código se ejecutará
            self.pantalla = pg.display.set_mode((1280,720), flags=pg.SHOWN)     # mostramos el display de pygame
        
# *BUCLE* #######################        TRANSICIÓN        ###################################        
        elif self.cambio_pantalla == 'transicion':  
            print(1)      
            match self.tipo_transicion[1]: # Usando Expresiones Regulares obtenemos 1t/2t/3t/m35
                case '1t':
                    self.t1_set.update()  # seguimos mostrando T1 durante la pantalla de carga
                case '2t':
                    self.t2_set.update()  # seguimos mostrando T2 durante la pantalla de carga
                case '3t':
                    self.t3_set.update()  # seguimos mostrando T3 durante la pantalla de carga
                
            self.t1_set.transicion()

            if self.t1_set.transparencia < 1:   
                self.cambio_pantalla = self.tipo_transicion[1]


# *BUCLE* #######################        1T        ###################################
        elif self.cambio_pantalla == '1t':
            
            if not self.t1_set.victoria_1t(self.t1_set.tablero)[0]\
                and self.t1_set.num_movimientos < 9:   # NO hay victoria
                self.t1_set.update()    # update está creado en T1_settings → t1_set (update es la forma correcta para ejcutar T1)

            else:                                                                       # SÍ hay victoria
                # Si gana el J1, lo guardamos en la DB
                if self.t1_set.jugador1.simbolo == self.t1_set.victoria_1t(self.t1_set.tablero)[1]:
                    db.añadirPuntuacion(db.returnActivo()[0],'T1',1)     # db: permanente
                    self.t1_set.jugador1.puntuacion += 1            # sesión: temporal

                # Si gana el J2, se guarda en la sesión    
                elif self.t1_set.jugador2.simbolo == self.t1_set.victoria_1t(self.t1_set.tablero)[1]:
                    self.t1_set.jugador2.puntuacion += 1 # sesión: temporal

                
                # else: Si hay empate no ocurre nada

                # Reinicio de ajustes
                self.t1_set.reinicio_1t()
                self.tipo_transicion = cte.transicion('transicion1t')
                self.cambio_pantalla = self.tipo_transicion[0]


# *BUCLE* #######################        2T        ###################################
        elif self.cambio_pantalla == '2t':
           
            if not self.t2_set.victoria_2t()[0]: # falta condición num mov 81 y empate ?

                self.t2_set.mini_victorias = self.t2_set.get_mini_victorias()   # comprobamos el estado actual del tablero
                                                                                # para añdir nuevas mini_victorias
                
                self.t2_set.update()        # como argumento le damos una lista de tuplas
                                            # cada elemento de la lista es una matriz ganada
                                            # la tupla corresponde a la fila y la columna

            else:
                if self.t2_set.jugador1.simbolo == self.t2_set.victoria_2t()[1]:
                    db.añadirPuntuacion(db.returnActivo()[0],'T2',1) 
                    self.t2_set.jugador1.puntuacion += 1 
                elif self.t2_set.jugador2.simbolo == self.t2_set.victoria_2t()[1]:
                    self.t2_set.jugador2.puntuacion += 1
                
                # Reinicio de ajustes
                self.t2_set.reinicio_2t()
                self.tipo_transicion = cte.transicion('transicion2t')
                self.cambio_pantalla = self.tipo_transicion[0]

        
# *BUCLE* #######################        3T        ###################################
        elif self.cambio_pantalla == '3t':
            if not self.t3_set.victoria_3t()[0]:
                self.t3_set.update()
            else:
                # Reinicio de ajustes
                print(1)
                self.t3_set.reinicio_3t()
                self.tipo_transicion = cte.transicion('transicion3t')
                self.cambio_pantalla = self.tipo_transicion[0]

        
# *BUCLE* #######################        EASTER_EGG        ###################################
        elif self.cambio_pantalla == 'easter_egg':
            self.easter_set.update(None)
            # Puntuación actual
            self.t2_set.mostrar_texto(self.pantalla, str(self.easter_set.jugador.puntuacion), cte.fuente_p1, 40, cte.BLANCO, (20, 20))
            # Best Score (Personal)
            self.t2_set.mostrar_texto(self.pantalla, 'Personal Score', cte.fuente_p1, 40, cte.BLANCO, (1040, 20))
            self.t2_set.mostrar_texto(self.pantalla, str(self.easter_set.jugador.personal_hs), cte.fuente_p1, 40, cte.BLANCO, (1140, 60))
            # Best Score (Global)
            self.t2_set.mostrar_texto(self.pantalla, 'Global Score', cte.fuente_p1, 40, cte.BLANCO, (1040, 100))
            self.t2_set.mostrar_texto(self.pantalla, str(self.easter_set.jugador.global_hs), cte.fuente_p1, 40, cte.BLANCO, (1140, 140))


# *BUCLE* #######################        M35        ###################################
        elif self.cambio_pantalla == 'm35':
            
            if not self.m35_set.victoria_m35()[0]: # and self.m35_set.return_num_mov() < 9:   # NO hay victoria
                self.m35_set.update()    # update está creado en M35_settings → t1_set (update es la forma correcta para ejcutar M35)

            else:                                                                       # SÍ hay victoria
                # Si gana el J1, lo gaurdamos en la DB
                if self.m35_set.jugador1.simbolo == self.m35_set.victoria_m35()[1]:
                    db.añadirPuntuacion(db.returnActivo()[0],'m35',1)     # db: permanente
                    self.m35_set.jugador1.puntuacion += 1            # sesión: temporal

                # Si gana el J2, se guarda en la sesión    
                elif self.m35_set.jugador2.simbolo == self.m35_set.victoria_m35()[1]:
                    self.m35_set.jugador2.puntuacion += 1 # sesión: temporal

                
                # else: Si hay empate no ocurre nada

                # Reinicio de ajustes
                self.m35_set.reinicio_m35()
                self.cambio_pantalla = 'refresh_m35' # nos vemos a una pantalla de carga
              
        # Pantalla de carga M35
        elif self.cambio_pantalla == 'refresh_m35':        
            self.m35_set.update()                # seguimos mostrando el juego durante la pantalla de carga
            self.m35_set.transicion()            # bajamos la opacidad para darle un efecto desvanecedor

            if self.m35_set.transparencia < 1:   # cuando la opacidad llega al mínimo
                self.cambio_pantalla = 'm35'     # se habilita poder jugar de nuevo  
            
        pg.display.update()
