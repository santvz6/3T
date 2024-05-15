import pygame as pg
import re
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

    def cambiar_turno(self):
        self.actual = self.jugador1 if self.jugador2 == self.actual else self.jugador2

    def jug_inicial(self):
        self.jug_ini = self.jugador1 if self.jugador2 == self.jug_ini else self.jugador2

    def victoria_m35(self):
        if self.actual.simbolo == 'J1':
            simb_prev = 'J2'
        else:
            simb_prev = 'J1'
        
        comb_ganadora = simb_prev*3
    # Verificar filas
        for fila in self.tablero:
            self.filas = ''
            for n in range(5):
                self.filas += str(fila[n])

            if re.search(comb_ganadora, self.filas):
                return (True, simb_prev)

    # Verificar columnas
        for n in range(5):
            self.columnas = ''
            for columna in self.tablero:
                self.columnas += str(columna[n])

            if re.search(comb_ganadora, self.columnas):
                return (True, simb_prev)

    # Verificar diagonales
    # Izq - der
        for i in range(5):
            ini = 6
            f = 6
            self.diagonal = ''
            match i:
                case 0:
                    ini = 0
                    f = 5
                case 1:
                    ini = 0
                    f = 4
                case 2:
                    ini = 0
                    f = 3
                case 3:
                    ini = 2
                    f = 5
                case 4:
                    ini = 1
                    f = 5

            for j in range(ini, f, 1):
                self.diagonal += str(self.tablero[j][(i+j)%5])
            
            if re.search(comb_ganadora, self.diagonal):
                return (True, simb_prev)
        
    #Der - izq
        for i in range(5):
            ini = 6
            f = 6
            self.diagonal2 = ''
            
            match i:
                case 0:
                    ini = 5
                    f = 0
                case 1:
                    ini = 4
                    f = 0
                case 2:
                    ini = 3
                    f = 0
                case 3:
                    ini = 5
                    f = 2
                case 4:
                    ini = 5
                    f = 1

            for j in range(ini, f, -1):
                self.diagonal2 += str(self.tablero[j-1][-(j-5+i)])
    
            if re.search(comb_ganadora, self.diagonal2):
                return (True, simb_prev)
        
        return (False, None)

    def restringir(self):
        for i in range(5):
            for j in range(5):
                m_pressed = pg.mouse.get_pressed()
                if 355+115*(i) < m_pressed[0] < 355+115*(i+1) and 120+115*j < m_pressed[1] < 120+115*(j+1):
                    centro = (i, j)
        fila = centro[0]
        columna = centro[1]
        restriccion = []
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                fila_restringida = fila + i
                columna_restringida = columna + j
                match fila_restringida:
                    case -1:
                        fila_restringida = 4
                    case 6:
                        fila_restringida = 0
                    
                match columna_restringida:
                    case -1:
                        columna_restringida = 4
                    case 6:
                        columna_restringida = 0
            
                restriccion.append((fila_restringida, columna_restringida))
        
        for coordenadas in restriccion:
            self.mostrar_texto(self.pantalla,str(1 +fila*3 + columna),cte.fuente_p1,35,cte.BLANCO_T,(410+110*coordenadas[0],165+110*coordenadas[1]))
                        

        #Queda encontrar una forma de pasar la lista restricción a coordenadas para mostrar el tablero de juego
        #Tmb incluir la función restringir cuando se recoja la casilla que elige el usuario
                      

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
            text_surface.set_alpha(color[3])  # render elimina la opacidad
            self.pantalla_trans.blit(text_surface, text_rect)

        elif pantalla_int == self.pantalla:
            self.pantalla.blit(text_surface, text_rect)

    def dibujar_m35(self):
        self.pantalla.blit(cte.fondo_m35,(0,0))
        for fila in range(5):
            for columna in range(5):
                m_pos = pg.mouse.get_pos()

                match self.tablero[fila][columna]:
                    # Los símbolos de los jugadores siempre estarán iluminados
                    case self.jugador1.simbolo:
                        self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,self.jugador1.color,(410+110*columna,165+110*fila))
                    case self.jugador2.simbolo:
                        self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,self.jugador2.color,(410+110*columna,165+110*fila))
                    # Las casillas sin jugar no siempre estarán iluminadas
                    case _:
                        # el cursor está encima → lo iluminamos de blanco
                        if 355+115*(columna) < m_pos[0] < 355+115*(columna+1) and 120+115*fila < m_pos[1] < 120+115*(fila+1):
                            self.mostrar_texto(self.pantalla,str(1 +fila*3 + columna),cte.fuente_p1,35,cte.BLANCO,(410+110*columna,165+110*fila))
                        # el cursor no está encima → lo coloreamos de blanco transparente
                        else:
                            self.mostrar_texto(self.pantalla_trans,str(1 +fila*3 + columna),cte.fuente_p1,35,cte.BLANCO2_T,(410+110*columna,165+110*fila))

    #Creo q no es necesaria
    def dibujar_m35_on(self):
        m_pos = pg.mouse.get_pos()
        for y in range(5):
            for x in range(5):
                if 385+115 * x < m_pos[0] < 385+115*(x + 1) and 150+115*y < m_pos[1] < 150+115*(y + 1):
                    if self.tablero[y][x] in [str(_) for _ in range(1,25)]:
                        self.mostrar_texto(self.pantalla,self.tablero[y][x],cte.fuente_p1,35,cte.BLANCO,(442.5+115*x,207.5+115*y))

                    elif self.tablero[y][x] == self.jugador1.simbolo:
                        self.mostrar_texto(self.pantalla,self.tablero[y][x],cte.fuente_p1,35,self.jugador1.color,(442.5+115*x,207.5+115*y))
                
                    else:
                        self.mostrar_texto(self.pantalla,self.tablero[y][x],cte.fuente_p1,35,self.jugador2.color,(442.5+115*x,207.5+115*y))

    def dibujar_elementos(self):
        m_pos = pg.mouse.get_pos()
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
        # Salir
        pg.draw.rect(self.pantalla_trans, cte.amarillo_t1_T,(50,25,150,55))
        pg.draw.rect(self.pantalla_trans, cte.BLANCO_T,(50,25,150,55),2)
        self.mostrar_texto(self.pantalla_trans, 'SALIR', cte.fuente_p1, 20, cte.BLANCO_T, (100,40))
        self.pantalla.blit(self.pantalla_trans, (0,0))
        # Salir_on
        if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
            pg.draw.rect(self.pantalla, cte.amarillo_t1,(50,25,150,55))
            pg.draw.rect(self.pantalla, cte.BLANCO,(50,25,150,55),2)
            self.mostrar_texto(self.pantalla, 'SALIR',cte.fuente_p1, 20, cte.BLANCO, (100,40))
        # Reniciar
        pg.draw.rect(self.pantalla_trans, cte.amarillo_t1_T,(1080,25,150,55))
        pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(1080,25,150,55),2)
        self.mostrar_texto(self.pantalla_trans, 'REINICIAR', cte.fuente_p1, 20, cte.BLANCO2_T, (1115,40))
        # Reiniciar_on
        if 1080 < m_pos[0] < 1230 and 25 < m_pos[1] < 80:
            pg.draw.rect(self.pantalla, cte.amarillo_t1,(1080,25,150,55))
            pg.draw.rect(self.pantalla, cte.BLANCO,(1080,25,150,55),2)
            self.mostrar_texto(self.pantalla, 'REINICIAR',cte.fuente_p1, 20, cte.BLANCO, (1115,40))
 
    def actualizar_m35_mouse(self):
        m_pos = pg.mouse.get_pos()
        for y in range(5):
            for x in range(5):
                if 355+115*(x) < m_pos[0] < 355+115*(x+1) and 120+115*y < m_pos[1] < 120+115*(y+1):
                # Validación casilla sin jugar
                    if self.tablero[y][x] in [str(_ + 1) for _ in range(25)]:
                        self.tablero[y][x] = self.actual.simbolo
                        self.cambiar_turno()
                        self.num_mov += 1
            
    def return_num_mov(self):
        return self.num_mov

    def transicion(self):
        if self.transparencia > 0:
            self.transparencia -= 5

        pg.draw.rect(self.pantalla_trans, (0,0,0,self.transparencia), (0,0,1280, 720))
        self.pantalla.blit(self.pantalla_trans, (0,0))



########################### TRAS UNA JUGADA VÁLIDA ###########################   
    def update(self):
        self.dibujar_m35()  # Fondo y tablero
        self.pantalla.blit(self.pantalla_trans, (0,0))
        self.pantalla_trans.fill((0,0,0,0))
        self.dibujar_elementos()  # Elementos
