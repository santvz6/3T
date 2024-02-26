import pygame as pg
import sys
from T1_settings import Tablero1
from Menu_settings import Menu
import cte

# Pantalla se encargará de establecer cada tipo de escenario y de
# seleccionar mediante update() que escenario cargar

class Pantalla:
    def __init__(self, pantalla, pantalla_trans):

        # Atributos de instancia
        self.pantalla = pantalla
        self.pantalla_trans = pantalla_trans
        self.cambio_pantalla = '1t' # pantalla actual

        # Instancias
        self.t1_set = Tablero1(self.pantalla, self.pantalla_trans)
        self.menu_set = Menu(self.pantalla, self.pantalla_trans)


    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
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
                        

        if self.cambio_pantalla == 'menu':
            self.menu_set.menu()
            self.menu_set.FondoMovimiento(cte.menu_boceto,600,400,600,200)

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
                    self.t1_set.jugador1.puntuacion += 1
                elif self.t1_set.jugador2.simbolo == self.t1_set.victoria_1t()[1]:
                    self.t1_set.jugador2.puntuacion += 1
                
                # Reinicio de ajustes
                self.t1_set.reinicio_1t()
                self.cambio_pantalla = 'refresh' # nos vemos a una pantalla de carga
              
        # Pantalla de carga
        elif self.cambio_pantalla == 'refresh':        
            self.t1_set.update2()
            self.t1_set.transicion() # bajamos la opacidad

            print(self.t1_set.transparencia)
            if self.t1_set.transparencia < 1: # cuando la opacidad llega al mínimo
                self.cambio_pantalla = '1t' # se habilita poder jugar de nuevo

        pg.display.update()