""" Easter_Egg.py
Este fichero contiene la creación de la clase EasterEgg. Este fichero contiene la creación de la clase EasterEgg, y además, 
la instancia del Jugador2. En este fichero contamos con el método update que será actualizado dentro del bucle de juego.


El fichero utiliza los siguientes módulos:
* from Settings.Jugador import Jugador2: para instanciar Jugador2 y todos sus métodos
* cte: para utilizar datos constantes guardados
"""

# Ficheros
import cte
from Settings.Jugador import Jugador2

class EasterEgg:
    """
    Clase encargada de establecer las actualizaciones necesarias
    del Jugador 2.
    """
    def __init__(self, pantalla):
        """
        El método instancia al Jugador del juego.
    
        Parámetros
        ----------
        pantalla : pygame.surface.Surface
            En ella mostramos todos los objetos pygame.
        """
        self.pantalla = pantalla
        self.jugador = Jugador2()
    
    def update(self, saltar: bool|None):
        self.pantalla.blit(cte.easter_fondo, (0,0))
        self.pantalla.blit(self.jugador.image,(self.jugador.rect.x,self.jugador.rect.y))
        self.jugador.update(saltar)
        
