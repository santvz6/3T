import pygame as pg
import sys
from T1_settings import Tablero1
from T2_settings import Tablero2
import cte

import UI_db.DataBase as db
from UI_db.ui_login import UiLogin


# Pantalla se encargará de establecer cada tipo de escenario y de
# seleccionar mediante update() que escenario cargar



class Pantalla:
    def __init__(self, pantalla, pantalla_trans, juego_inicial, main):

        # Atributos de instancia
        self.pantalla = pantalla
        self.pantalla_trans = pantalla_trans
        #self.cambio_pantalla = juego_inicial # pantalla actual
        self.cambio_pantalla = '2t'
        self.main = main # Contiene todos los self de main


        # Instancias
        self.t1_set = Tablero1(self.pantalla, self.pantalla_trans)
        self.t2_set = Tablero2(self.pantalla, self.pantalla_trans)

    # Juego elegido viene de → UIMenu
    # Como es una variable guardada, no podemos usarla en 
    # el método init. Necesitamos que en cada vuelta del bucle
    # sepamos con anterioridad (por eso esta al principio),
    # dónde vamos a mostrar el display.
    # self.cambio_pantalla = juego_elegido
    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                db.set_inactivo()
                db.mostrarDatos()
                sys.exit()

            if self.cambio_pantalla == '1t':
                # CLICK DERECHO
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  
                    m_pos = pg.mouse.get_pos()
                    if not self.t1_set.victoria_1t()[0]:                     
                        self.t1_set.actualizar_1t_mouse()
                        
                        
                    
                    # Botón de salir
                    if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
                        self.cambio_pantalla = 'menu'

                # KEYDOWN DE UNA TECLA
                if event.type == pg.KEYDOWN:
                    if pg.K_1 <= event.key <= pg.K_9:
                        self.t1_set.actualizar_1t_teclas(int(event.unicode)) #recibe el número recibido
                        self.t1_set.update2()

        if self.cambio_pantalla == 'login':
            pass
    
        elif self.cambio_pantalla == 'menu':

            # https://stackoverflow.com/questions/10466590/hiding-pygame-display
            # En un foro de stack overflow podemos ver como ocultar una 
            # pantalla en pygame sin necesidad de hacer: pygame.quit()
            self.pantalla = pg.display.set_mode((1280,720), flags=pg.HIDDEN)
            
            self.main.ui.menu.deiconify()
            self.main.ui.mainloop()
        
            
            #self.cambio_pantalla = juego_elegido # pantalla actual
            self.pantalla = pg.display.set_mode((1280,720), flags=pg.SHOWN) # mostramos la ventana de pygame

        # Juego 1t
        elif self.cambio_pantalla == '1t':
            # --- Juego en curso ---
            if not self.t1_set.victoria_1t()[0] and self.t1_set.return_num_mov() < 9:
                self.t1_set.update2()
                self.t1_set.dibujar_t1_on() # mouse ON algún número del tablero

            # Se produce una victoria
            else:
                # Compobar que jugador ha ganado
                if self.t1_set.jugador1.simbolo == self.t1_set.victoria_1t()[1]:
                    db.puntuar_db(db.return_activo()[0],'T1',1) # permanente
                    self.t1_set.jugador1.puntuacion += 1 # temporal
                elif self.t1_set.jugador2.simbolo == self.t1_set.victoria_1t()[1]:
                    self.t1_set.jugador2.puntuacion += 1 # temporal
                
                # Reinicio de ajustes
                self.t1_set.reinicio_1t()
                self.cambio_pantalla = 'refresh' # nos vemos a una pantalla de carga
              
        # Pantalla de carga
        elif self.cambio_pantalla == 'refresh':        
            self.t1_set.update2()
            self.t1_set.transicion() # bajamos la opacidad

            print(self.t1_set.transparencia)
            if self.t1_set.transparencia < 1: # cuando la opacidad llega al mínimo
                print('ENTRE:', self.t1_set.transparencia)
                self.cambio_pantalla = '1t' # se habilita poder jugar de nuevo
        elif self.cambio_pantalla == '2t':
            self.t2_set.dibujar()
        pg.display.update()