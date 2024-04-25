import pygame as pg

# Ficheros
import cte

# Para ejecutar código desde main
import UI_db.DataBase as db
from Settings.Jugador import Jugador



class Tablero1:
  def __init__(self, pantalla, pantalla_trans):

    # Creación del tablero
    self.tablero = [[str((n+1)+(m*3)) for n in range(3)] for m in range(3)]
    #print(self.tablero)

    # Instancias iniciales
    self.jugador1 = Jugador('Jug1','J1', 0, cte.amarillo_t1)
    self.jugador2 = Jugador('Jug2', 'J2', 0, cte.azul_1)

    # Atributos de instancia
    self.pantalla = pantalla 
    self.pantalla_trans = pantalla_trans
    self.actual = self.jugador1 # Primer movimiento
    self.jug_ini = self.jugador1 # 

    self.transparencia = 255
    self.num_mov = 0
    

########################### LÓGICA DEL JUEGO ORIENTADA A PYTHON VANILLA ###########################

  def turno(self):
    self.actual = self.jugador1 if self.jugador2 == self.actual else self.jugador2

  def jug_inicial(self):
    # Sirve para alternar quién comienza en cada nueva partida
    self.jug_ini = self.jugador1 if self.jugador2 == self.jug_ini else self.jugador2


  def victoria_1t(self):
    # Verificar filas
    for fila in self.tablero:
      if fila[0] == fila[1] == fila[2]:
        return True, fila[0]

    # Verificar columnas
    for columna in range(3):
      if self.tablero[0][columna] == self.tablero[1][columna] == self.tablero[2][columna]:
        return (True, self.tablero[0][columna])

    # Verificar diagonales
    if self.tablero[0][0] == self.tablero[1][
        1] == self.tablero[2][2]:
      return (True, self.tablero[0][0])
    
    if self.tablero[0][2] == self.tablero[1][
        1] == self.tablero[2][0]:
      return (True, self.tablero[0][2])

    return (False, None)
  
  def reinicio_1t(self):
    self.tablero = [[str((n+1)+(m*3)) for n in range(3)] for m in range(3)]
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
      

  def dibujar_1t(self):
    self.pantalla.blit(cte.fondo_1t,(0,0))
    for fila in range(3):
      for columna in range(3):

        m_pos = pg.mouse.get_pos() # cada iteración hacemos una comprobación

        if self.tablero[fila][columna] == self.jugador1.simbolo:
          self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,self.jugador1.color,(560+80*columna,259+80*fila))
                                 
        elif self.tablero[fila][columna] == self.jugador2.simbolo:
          self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,self.jugador2.color,(560+80*columna,259+80*fila))
        # Casilla sin jugar
        else:
          # el cursor está encima → lo coloreamos de blanco
          if 532+80.6*(columna) < m_pos[0] < 524+80.6*(columna+1) and 240+80*fila < m_pos[1] < 240+80.6*(fila+1):
            self.mostrar_texto(self.pantalla,self.tablero[fila][columna],cte.fuente_p1,35,cte.BLANCO,(560+80*columna,259+80*fila))
          # el cursor no está encima → lo coloreamos de blanco transparente
          else:
            self.mostrar_texto(self.pantalla_trans,self.tablero[fila][columna],cte.fuente_p1,35,cte.BLANCO_T,(560+80*columna,259+80*fila))
            

    

  def dibujar_punt(self):
    # Simbolo
    self.mostrar_texto(self.pantalla,self.jugador1.simbolo, cte.fuente_p1, 35, cte.BLANCO,(545, 600))
    self.mostrar_texto(self.pantalla,self.jugador2.simbolo, cte.fuente_p1, 35, cte.BLANCO,(665, 600))
    # Separador
    self.mostrar_texto(self.pantalla,':', None, 35, cte.BLANCO,(575, 610))
    self.mostrar_texto(self.pantalla,':', None, 35, cte.BLANCO,(695, 610))
    # Puntuación
    self.mostrar_texto(self.pantalla, str(self.jugador1.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(600, 600))
    self.mostrar_texto(self.pantalla, str(self.jugador2.puntuacion), cte.fuente_p1, 35, cte.BLANCO,(720, 600))



  # Actualización el tablero cuando se hace click
  def actualizar_1t_mouse(self):
    m_pos = pg.mouse.get_pos()
    for y in range(3):
      for x in range(3):
        if 532+80.6*(x) < m_pos[0] < 524+80.6*(x+1) and 240+80*y < m_pos[1] < 240+80.6*(y+1):
          # Validación casilla sin jugar
          if self.tablero[y][x] in [str(_ + 1) for _ in range(9)]:
            self.tablero[y][x] = self.actual.simbolo
            self.turno()
            self.num_mov += 1
  
          
  def actualizar_1t_teclas(self,unicode):
    # Conversión de elemento a fila y columna
    fila = (unicode - 1) // 3
    columna = (unicode - 1) % 3
    if self.tablero[fila][columna] in [str(_ + 1) for _ in range(9)]:
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
  def boton(self): # Botón en reposo
    # Transparente
    pg.draw.rect(self.pantalla_trans, cte.amarillo_t1_T,(50,25,150,55))
    pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(50,25,150,55),2)
    self.mostrar_texto(self.pantalla_trans, 'SALIR', cte.fuente_p1, 20, cte.BLANCO2_T, (100,40))

    pg.draw.rect(self.pantalla_trans, cte.amarillo_t1_T,(1080,25,150,55))
    pg.draw.rect(self.pantalla_trans, cte.BLANCO2_T,(1080,25,150,55),2)
    self.mostrar_texto(self.pantalla_trans, 'REINICIAR', cte.fuente_p1, 20, cte.BLANCO2_T, (1115,40))
        

  def boton_on(self): # Mouse en el botón
    m_pos = pg.mouse.get_pos()
    if 50 < m_pos[0] < 200 and 25 < m_pos[1] < 80:
      # Sólido
      pg.draw.rect(self.pantalla, cte.amarillo_t1,(50,25,150,55))
      pg.draw.rect(self.pantalla, cte.BLANCO,(50,25,150,55),2)
      self.mostrar_texto(self.pantalla, 'SALIR',cte.fuente_p1, 20, cte.BLANCO, (100,40))

    if 1080 < m_pos[0] < 1230 and 25 < m_pos[1] < 80:
      # Sólido
      pg.draw.rect(self.pantalla, cte.amarillo_t1,(1080,25,150,55))
      pg.draw.rect(self.pantalla, cte.BLANCO,(1080,25,150,55),2)
      self.mostrar_texto(self.pantalla, 'REINICIAR',cte.fuente_p1, 20, cte.BLANCO, (1115,40))



########################### TRAS UNA JUGADA VÁLIDA ###########################   
  def update(self):
    self.dibujar_1t() # Fondo y tablero
    self.dibujar_punt() # Puntuación
    
    self.pantalla.blit(self.pantalla_trans, (0,0))
    self.pantalla_trans.fill((0, 0, 0, 0))# reinicio de superficie, se acumulan los .blit() 

    self.boton() # Botón de salir
    self.boton_on() # Botón encima
