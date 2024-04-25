import pygame as pg

# Ficheros
import cte

# Para ejecutar código desde main
import UI_db.DataBase as db
from Settings.Jugador import Jugador


class M35:
    def __init__(self, pantalla, pantalla_trans):
        
        # Creación del tablero
        self.tablero = [[str((n+1)+(m*5)) for n in range(5)] for m in range(5)]

        #print(self.tablero)

        # Instancias iniciales
        self.jugador1 = Jugador('Jug1','J1', 0, cte.amarillo_t1)
        self.jugador2 = Jugador('Jug2', 'J2', 0, cte.azul_1)

        # Atributos de instancia
        self.pantalla = pantalla 
        self.pantalla_trans = pantalla_trans
        self.actual = self.jugador1 # Primer movimiento
        self.jug_ini = self.jugador1 # Cambio de

        self.transparencia = 255
        self.num_mov = 0

########################### LÓGICA DEL JUEGO ORIENTADA A PYTHON VANILLA ###########################

    def turno(self):
        self.actual = self.jugador1 if self.jugador2 == self.actual else self.jugador2

    def jug_inicial(self):
        self.jug_ini = self.jugador1 if self.jugador2 == self.jug_ini else self.jugador2

    def victoria_m35(self):
        # Verificar filas
        filas = ''
        for fila in self.tablero:
            for n in range(5):
                filas += str(fila[n])
            filasx2 = filas*2

            if 'J1'*3 in filasx2:
                return (True, 'J1')
            if 'J2'*3 in filasx2:
                return (True, 'J2')

        # Verificar columnas
        columnas = ''
        for columna in self.tablero:
            for n in range(5):
                columnas += str(columna[n])
            columnasx2 = columna*2

            if 'J1'*3 in columnasx2:
                return (True, 'J1')
            if 'J2'*3 in columnasx2:
                return (True, 'J2')
            
        # Verificar diagonales
        #Izq - der
        for i in range(5):
            diagonal = ''
            for j in range(5):
                diagonal += str(self.tablero[j][(i+j)%5])
            diagonalx2 = diagonal*2

            if 'J1'*3 in diagonalx2:
                return (True, 'J1')
            if 'J2'*3 in diagonalx2:
                return (True, 'J2')
        #Der - izq
        for i in range(5, 0, -1):
            diagonal = ''
            for j in range(5, 0, -1):
                diagonal += str(self.tablero[j-1][-(j-5+i)])
                diagonalx2 = diagonal*2

            if 'J1'*3 in diagonalx2:
                return (True, 'J1')
            if 'J2'*3 in diagonalx2:
                return (True, 'J2')
        
        return (False, None)

    def reinicio_m35(self):
        self.tablero = [[str((n+1)+(m*5)) for n in range(5)] for m in range(5)]
        self.num_mov = 0
        self.jug_inicial()
        self.actual = self.jug_ini
        self.transparencia = 255

########################### LÓGICA DEL JUEGO ORIENTADA A PYGAME ###########################


    def mostrar_texto(self,pantalla_int, texto, fuente, tamaño, color, posicion):
        # Crear un objeto de texto
        font = pg.font.Font(fuente, tamaño)
        text_surface = font.render(texto, True, color)
        
        # Obtener el rectángulo del texto y configurar la posición
        text_rect = text_surface.get_rect()
        text_rect.topleft = posicion

        # Dibujar el texto en la pantalla
        if pantalla_int == self.pantalla_trans:
            text_surface.set_alpha(color[3]) # render elimina la opacidad
            self.pantalla_trans.blit(text_surface, text_rect)

        elif pantalla_int == self.pantalla:
            self.pantalla.blit(text_surface, text_rect)

    def dibujar_m35(self):
        self.pantalla.blit(cte.fondo_m35,(0,0))
        for fila in range(5):
            for columna in range(5):
                if self.tablero[fila][columna] == self.jugador1.simbolo:
                    self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,self.jugador1.color,(410+110*columna,165+110*fila))
                             
                elif self.tablero[fila][columna] == self.jugador2.simbolo:
                    self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,self.jugador2.color,(410+110*columna,165+110*fila))

                else:
                    self.mostrar_texto(self.pantalla_trans,self.tablero[fila][columna],cte.fuente_p1,35,cte.BLANCO_T,(410+110*columna,165+110*fila))
    
    def dibujar_m35_on(self):
        m_pos = pg.mouse.get_pos()
        for y in range(5):
            for x in range(5):
                if 390+110*(x) < m_pos[0] < 390+110*(x+1) and 145+110*y < m_pos[1] < 145+110*(y+1):
                    if self.tablero[y][x] in [str(_) for _ in range(1,25)]:
                        self.mostrar_texto(self.pantalla,self.tablero[y][x],cte.fuente_p1,35,cte.BLANCO,(410+110*x,165+110*y))

                    elif self.tablero[y][x] == self.jugador1.simbolo:
                        self.mostrar_texto(self.pantalla,self.tablero[y][x],cte.fuente_p1,35,self.jugador1.color,(410+110*x,165+110*y))
                
                    else:
                        self.mostrar_texto(self.pantalla,self.tablero[y][x],cte.fuente_p1,35,self.jugador2.color,(410+110*x,165+110*y))

    def dibujar_punt(self):
        # Simbolo
        self.mostrar_texto(self.pantalla,self.jugador1.simbolo, cte.fuente_p1, 35, cte.BLANCO,(1025, 600))
        self.mostrar_texto(self.pantalla,self.jugador2.simbolo, cte.fuente_p1, 35, cte.BLANCO,(1200, 600))
        # Separador
        self.mostrar_texto(self.pantalla,':', None, 35, cte.BLANCO,(1055, 610))
        self.mostrar_texto(self.pantalla,'-', None, 35, cte.BLANCO,(1115, 610))
        self.mostrar_texto(self.pantalla,':', None, 35, cte.BLANCO,(1185, 610))
        # Puntuación
        self.mostrar_texto(self.pantalla, str(self.jugador1.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(1080, 600))
        self.mostrar_texto(self.pantalla, str(self.jugador2.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(1145, 600))

    def actualizar_m35_mouse(self):
        m_pos = pg.mouse.get_pos()
        for y in range(5):
            for x in range(5):
                if 410+110*(x) < m_pos[0] < 410+110*(x+1) and 165+110*y < m_pos[1] < 165+110*(y+1):
                # Validación casilla sin jugar
                    if self.tablero[y][x] in [str(_ + 1) for _ in range(25)]:
                        self.tablero[y][x] = self.actual.simbolo
                        self.turno()
                        self.num_mov += 1
            
    def actualizar_m35_teclas(self,unicode):
    # Conversión de elemento a fila y columna
        fila = (unicode - 1) // 3
        columna = (unicode - 1) % 3
        if self.tablero[fila][columna] in [str(_ + 1) for _ in range(25)]:
            self.tablero[fila][columna] = self.actual.simbolo
            self.turno()
            self.num_mov += 1
  
    def return_num_mov(self):
        return self.num_mov

    def transicion(self):
        if self.transparencia > 0:
            self.transparencia -= 5

        pg.draw.rect(self.pantalla_trans, (0,0,0,self.transparencia), (0,0,1280, 720))
        self.pantalla.blit(self.pantalla_trans, (0,0))



########################### BOTONES DURANTE EL JUEGO ###########################    
    def salir_bot(self): # Botón en reposo
        # Transparente
        pg.draw.rect(self.pantalla_trans, cte.amarillo_t1_T,(50,25,150,55))
        pg.draw.rect(self.pantalla_trans, cte.BLANCO_T,(50,25,150,55),2)
        self.mostrar_texto(self.pantalla_trans, 'SALIR', cte.fuente_p1, 20, cte.BLANCO_T, (100,40))
        self.pantalla.blit(self.pantalla_trans, (0,0))
        
    def salir_on(self): # Mouse en el botón
        m_pos = pg.mouse.get_pos()
        if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
        # Sólido
            pg.draw.rect(self.pantalla, cte.amarillo_t1,(50,25,150,55))
            pg.draw.rect(self.pantalla, cte.BLANCO,(50,25,150,55),2)
            self.mostrar_texto(self.pantalla, 'SALIR',cte.fuente_p1, 20, cte.BLANCO, (100,40))


########################### TRAS UNA JUGADA VÁLIDA ###########################   
    def update2(self):
        self.dibujar_m35() # Fondo y tablero
        self.dibujar_punt() # Puntuación
        self.salir_bot() # Botón de salir
        self.salir_on() # Botón encima

        # reinicio de superficie |
        # se acumulan los .blit() 
        self.pantalla_trans.fill((0, 0, 0, 0))