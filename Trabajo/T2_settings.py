import pygame as pg
from Jugador import Jugador
import cte
import UI_db.DataBase as db
import numpy as np

class Tablero2:
    def __init__(self, pantalla, pantalla_trans):

        # Creación del tablero

        # Numpy trata las cadenas de caracteres como matrices de caracteres Unicode.
        # https://stackoverflow.com/questions/55377213/numpy-taking-only-first-character-of-string
        self.tablero = np.array([[[[str((j+1)+(i*3)) for j in range(3)] for i in range(3)] for t in range(3)] for k in range(3)], 
                                dtype=np.dtype('U2')) # Establecemos la longitud de datos hasta 2 (usaremos 'J1' y 'J2')

        # i → filas                 para acceder a un elemento → [k, t, i, j],
        # j → columnas              equivale a → [matriz_f, matriz_c, fila, columna]
        # k → matriz_f
        # t → matriz_c

        # str((j*1)+(i*9)+(t*3)+(k*27) + 1)     # matriz del 1 al 81
        # str((j+1)+(i*3))                      # matriz del 1 al 9, 9 veces

        # Instancias iniciales
        self.jugador1 = Jugador('Jug1','J1', 0, cte.amarillo_t2)
        self.jugador2 = Jugador('Jug2', 'J2', 0, cte.gris_t2)

        # Atributos de instancia
        self.pantalla = pantalla 
        self.pantalla_trans = pantalla_trans
        self.actual = self.jugador1 # Define quién está jugando actualmente
        self.jug_ini = self.jugador1 # Guarda solamente quién hizo el primer movimiento

        self.transparencia = 255
        self.num_mov = 0
        self.movimiento = (-1,-1)

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


    def dibujar_2t(self, mini_victorias):
        #print('DIMENSIONES: ', self.tablero.shape)
        self.pantalla.blit(cte.fondo_2t,(0,0))
        for matriz_f in range(3):
            for matriz_c in range(3):
                for fila in range(3):
                    for columna in range(3):
                        
                        m_pos = pg.mouse.get_pos()
                        #print(self.tablero)
                        x = 350 + 200*matriz_c+columna*200/3    # la 'x' se mueve por columnas
                        y = 110 + 200*matriz_f+fila*200/3       # la 'y' se mueve por filas
                        #print(self.tablero[matriz_f, matriz_c, fila, columna])

                        # Dibujar matriz con minivictoria
                        if (matriz_f, matriz_c) in mini_victorias:
                            if self.tablero[matriz_f, matriz_c, 0, 0] == self.jugador1.simbolo:
                                self.mostrar_texto(self.pantalla,self.jugador1.simbolo,cte.fuente_p1,120,self.jugador1.color,
                                                   (390 + 200*matriz_c,115 + 190*matriz_f))
                            else:
                                self.mostrar_texto(self.pantalla,self.jugador2.simbolo,cte.fuente_p1,120,self.jugador2.color,
                                                   (390 + 200*matriz_c,115 + 190*matriz_f))
                                
                        # Dibujar matriz sin minivictoria
                        else:
                            if self.tablero[matriz_f, matriz_c, fila, columna] == self.jugador1.simbolo:
                                self.mostrar_texto(self.pantalla,self.tablero[matriz_f, matriz_c, fila, columna],cte.fuente_p1,35,self.jugador1.color,(x+10, y))
                                                
                            elif self.tablero[matriz_f, matriz_c, fila, columna] == self.jugador2.simbolo:
                                self.mostrar_texto(self.pantalla,self.tablero[matriz_f, matriz_c, fila, columna],cte.fuente_p1,35,self.jugador2.color,(x+10, y))
                            
                            # Casillas no jugadas
                            else:
                                # Cursor encima
                                if x < m_pos[0] < x+200/3  and y < m_pos[1] < y+200/3:
                                    self.mostrar_texto(self.pantalla,self.tablero[matriz_f, matriz_c, fila, columna],cte.fuente_p1,35,cte.BLANCO,(x+10, y))
                                # Casillas sin cursor
                                else:
                                    if matriz_f == self.movimiento[0] and matriz_c == self.movimiento[1]:
                                        self.mostrar_texto(self.pantalla_trans,self.tablero[self.movimiento[0], self.movimiento[1], fila, columna],cte.fuente_p1,35,cte.BLANCO2_T,(x+10, y))
                                    # Incluye self.movimiento (-1, -1 → nunca coincide)
                                    else:
                                        self.mostrar_texto(self.pantalla_trans,self.tablero[matriz_f, matriz_c, fila, columna],cte.fuente_p1,35,cte.BLANCO_T,(x+10, y))                                    
                                
    def turno(self):
        # que te obligue a jugar en tal matriz
        self.actual = self.jugador1 if self.jugador2 == self.actual else self.jugador2


  # Actualización el tablero cuando se hace click
    def actualizar_2t_mouse(self, mini_victorias):
        m_pos = pg.mouse.get_pos()
        for matriz_f in range(3):
            for matriz_c in range(3):
                for fila in range(3):
                    for columna in range(3):

                        if self.movimiento == (-1, -1): 
                            x = 350 + 200*matriz_c+columna*200/3    # la 'x' se mueve por columnas / quite 10px (350) para hacerlo más preciso
                            y = 110 + 200*matriz_f+fila*200/3       # la 'y' se mueve por filas
                            
                        else:
                            x = 350 + 200*self.movimiento[1]+columna*200/3
                            y = 110 + 200*self.movimiento[0]+fila*200/3

                        if x < m_pos[0] < x+200/3  and y < m_pos[1] < y+200/3:
                            if (matriz_f, matriz_c) not in mini_victorias:
                                # Restricción de movimiento Nula
                                if self.movimiento == (-1, -1):
                                    # Validación casilla sin jugar
                                    if self.tablero[matriz_f, matriz_c, fila, columna] in [str(_ + 1) for _ in range(9)]:
                                        self.tablero[matriz_f, matriz_c, fila, columna] = self.actual.simbolo

                                        # Pasamos de una restricción (-1, -1) → (fila, columna)
                                        if (fila, columna) not in mini_victorias:
                                            self.movimiento = (fila, columna)   # la fila y columna determinará 
                                                                                # la matriz que se deberá jugar
                                            self.turno()

                                        # Pasamos de una restricción (-1, -1) → (-1, -1)
                                        # Si ya teniamos (-1, -1) y se selecciona otra vez una matriz ganada
                                        # cambiaremos de turno y establecemos (-1, -1) de nuevo
                                        else:
                                            print('Donde quieras')
                                            self.movimiento = (-1, -1)
                                            self.turno()


                                # Restricción de movimiento definida      
                                else:
                                    # Validación casilla sin jugar
                                    if self.tablero[self.movimiento[0], self.movimiento[1], fila, columna] in [str(_ + 1) for _ in range(9)]:
                                        self.tablero[self.movimiento[0], self.movimiento[1], fila, columna] = self.actual.simbolo
                                        # Validación de restricción permitida
                                        if (fila, columna) not in mini_victorias:
                                            self.movimiento = (fila, columna)   # la fila y columna determinará 
                                                                                # la matriz que se deberá jugar
                                            self.turno()
                                        else:
                                            print('Donde quieras')
                                            self.movimiento = (-1, -1)  # no le damos reestricción, si intenta jugar una matriz
                                                                        # ganada no podrá → está completa [['J1', 'J1', 'J1'],...]
                                            self.turno()
                            
                            

    def matriz_ganada(self, matriz_f, matriz_c, ganador):
        # Rellenamos toda una matriz de 3x3 con el simbolo ganador
            for fila_n in range(3):
                for columna_n in range(3):
                    self.tablero[matriz_f, matriz_c, fila_n, columna_n] =  ganador
                            


    def mini_victorias(self):
        mini_victorias = []
        for matriz_f in range(3):
            for matriz_c in range(3):

                # Verificar filas
                for fila in self.tablero[matriz_f, matriz_c]:
                    if fila[0] == fila[1] == fila[2]:
                        self.matriz_ganada(matriz_f, matriz_c, fila[0])
                        mini_victorias.append((matriz_f, matriz_c))

                # Verificar columnas
                for columna in range(3):
                    if self.tablero[matriz_f, matriz_c, 0, columna] == self.tablero[matriz_f, matriz_c, 1, columna] == self.tablero[matriz_f, matriz_c, 2, columna]:
                        self.matriz_ganada(matriz_f, matriz_c, self.tablero[matriz_f, matriz_c, 0, columna])
                        mini_victorias.append((matriz_f, matriz_c))
                    
                # Verificar diagonales
                if self.tablero[matriz_f, matriz_c, 0, 0] == self.tablero[matriz_f, matriz_c, 1, 1] == self.tablero[matriz_f, matriz_c, 2, 2]:
                    self.matriz_ganada(matriz_f, matriz_c, self.tablero[matriz_f, matriz_c, 0, 0])
                    mini_victorias.append((matriz_f, matriz_c))
                    
                if self.tablero[matriz_f, matriz_c, 0, 2] == self.tablero[matriz_f, matriz_c, 1, 1] == self.tablero[matriz_f, matriz_c, 2, 0]:
                    self.matriz_ganada(matriz_f, matriz_c, self.tablero[matriz_f, matriz_c, 0, 2])
                    mini_victorias.append((matriz_f, matriz_c))
                
        return mini_victorias




    def victoria_2t(self, mini_victorias):
        
        # Transformación en un array de 3x3
        victoria = np.array([[a*3+b for b in range(3)] for a in range(3)], dtype=np.dtype('U2'))
        for (fila, columna) in mini_victorias:
            victoria[fila, columna] = self.tablero[fila, columna, 0, 0]

    ### MISMA SINTAXIS QUE EN T1 ###

        # Verificar filas
        for fila in victoria:
            if fila[0] == fila[1] == fila[2]:
                return True, fila[0]

        # Verificar columnas
        for columna in range(3):
            if victoria[0][columna] == victoria[1][columna] == victoria[2][columna]:
                return (True, victoria[0][columna])  
                    
        # Verificar diagonales
        if victoria[0][0] == victoria[1][1] == victoria[2][2]:
            return (True, victoria[0][0])
           
        if victoria[0][2] == victoria[1][1] == victoria[2][0]:
            return (True, victoria[0][2])         
          
        return (False, None)
    
    def jug_inicial(self):
        # Sirve para alternar quién comienza en cada nueva partida
        self.jug_ini = self.jugador1 if self.jugador2 == self.jug_ini else self.jugador2


    def reinicio_2t(self):
        self.tablero = np.array([[[[str((j+1)+(i*3)) for j in range(3)] for i in range(3)] for t in range(3)] for k in range(3)], 
                                dtype=np.dtype('U2'))
        self.num_mov = 0
        self.jug_inicial()          # camviamos quién empieza en la nueva ronda 
        self.actual = self.jug_ini  # y lo registramos
        self.transparencia = 255
        self.movimiento = (-1, -1)
        


    def update(self, mini_victorias):
        self.dibujar_2t(mini_victorias)

        self.pantalla.blit(self.pantalla_trans, (0,0))
        self.pantalla_trans.fill((0, 0, 0, 0))
    
        self.salir_bot() # Botón de salir
        self.salir_on() # Botón encima
        self.dibujar_punt()


########################### BOTONES DURANTE EL JUEGO ###########################    
    def salir_bot(self): # Botón en reposo
        # Transparente
        pg.draw.rect(self.pantalla_trans, cte.naranja_t2_T,(85,25,150,55))
        pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(85,25,150,55),2)
        self.mostrar_texto(self.pantalla_trans, 'SALIR', cte.fuente_p1, 20, cte.BLANCO2_T, (135,40))
        #self.pantalla.blit(self.pantalla_trans, (0,0))
    

    def salir_on(self): # Mouse en el botón
        m_pos = pg.mouse.get_pos()
        if 85 < m_pos[0] < 235 and 25 < m_pos[1] < 80:
            # Sólido
            pg.draw.rect(self.pantalla, cte.naranja_t2,(85,25,150,55))
            pg.draw.rect(self.pantalla, cte.BLANCO,(85,25,150,55),2)
            self.mostrar_texto(self.pantalla, 'SALIR',cte.fuente_p1, 20, cte.BLANCO, (135,40))

########################### TEXTO ###########################
    def dibujar_punt(self):
        # Simbolo
        self.mostrar_texto(self.pantalla,self.jugador1.simbolo, cte.fuente_p1, 35, cte.BLANCO,(90, 300))
        self.mostrar_texto(self.pantalla,self.jugador2.simbolo, cte.fuente_p1, 35, cte.BLANCO,(210, 300))
        
        # Puntuación
        self.mostrar_texto(self.pantalla, str(self.jugador1.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(95, 390))
        self.mostrar_texto(self.pantalla, str(self.jugador2.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(215, 390))