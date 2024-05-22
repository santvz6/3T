""" main.py
Este fichero contiene la creación de la clase Game. La clase Game es la clase principal que controla el flujo del juego, 
la actualización de los estados y que contiene las instancias de los elementos gráficos.


El fichero utiliza los siguientes módulos:
* from Pantalla import Pantalla: usado para instanciar la pantalla donde se mostrarán todos los elementos Pygame
* from UI_db.ui_login import UiLogin: usado para instanciar la pantalla del Login creada en customtkinter
* UI_db.DataBase:  contiene el código encargado de administrar la tabla de usuarios.

Para utilizar el código es necesaria la instalación de las siguientes librerías en nuestro entorno virtual:
* pygame: utilizada para la creación del display para mostrar todos los correspondientes elementos
"""

# Módulos
from Pantalla import Pantalla
from UI_db.DataBase import db_principal as db
from UI_db.ui_login import UiLogin

# Librerías
import pygame as pg

class Game:
    """
    En main tendremos el código principal guardado en la clase Game
    El método __init__ recogerá las instancias de clases e iniciará pg.init()
    El método run se encargará de establecer el reloj de pygame y de actualizar en cada iteración la pantalla
    """
    def __init__(self, WIDTH=1280, HEIGTH=720):
        """
        Constructor de la clase. Aquí se inicializan varios atributos y se crean las instancias de todos los ajustes de cada juego creado.

        Parámetros
        ----------
        WIDTH : int
            Ancho de la pantalla.
        HEIGTH : int
            Altura de la pantalla.
        """

        db.crearTabla('USUARIOS')  # Creación Tabla Usuarios en la db
        db.setInactivo()           # Toda sesión abierta se cierra

        # No podemos usar Pantalla - No ha sido instanciada
        self.juego_inicial = ''     # en UiMenu definimos el primer juego (Antes de instanciar Pantalla)
                                    # Posteriormente UiMenu usará pantalla_actual.cambio_pantalla (Pantalla está instanciada)
        
        self.ui = UiLogin(self)     # Primera instancia CTk
        self.ui.mainloop()          # bucle principal CTk

        pg.init()                   # PyGame se inicia cuándo se hace .quit() del loop CTk

        pg.display.set_caption('3T')
        self.pantalla = pg.display.set_mode((WIDTH, HEIGTH))            # Display PyGame
        self.pantalla_trans = pg.Surface((WIDTH, HEIGTH), pg.SRCALPHA)  # Superficie que admite colores transparentes
                                                                        # tratada como una pantalla que será .blit() en self.pantalla
                                                                        # en cada iteración habrá que limpiarla .fill((0,0,0,0))
        
        # Se instancia con un juego inicial
        # Se instancia con el atributo UI (usado en las interfaces CTk) para interconectar interfaces
        self.pantalla_actual = Pantalla(self.pantalla, self.pantalla_trans, self.juego_inicial, self.ui)
        
        self.clock = pg.time.Clock()    # Instancia de Clock: Actualizaciones/Iteraciones por segundo

    def run(self, FPS=60):
        """
        Realiza las correspondientes actualizaciones de nuestra pantalla.
        Es el bucle principal de nuestros juegos.
        """
        while True:  
            self.pantalla_actual.update()   # actualizamos la pantalla por cada iteración del bucle
            self.clock.tick(FPS)            # 60 iteraciones por segundo

# Usamos tamaño HD de pantalla
game = Game()   
game.run() 

