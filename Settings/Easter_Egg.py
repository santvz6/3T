# Ficheros
import cte
import pickle

# Para ejecutar código desde main
from Settings.Jugador import Jugador2
from UI_db.DataBase import db_principal as db

class EasterEgg:
    def __init__(self, pantalla, pantalla_trans):
        self.pantalla = pantalla
        self.pantalla_trans = pantalla_trans

        self.jugador = Jugador2(self.pantalla)

    def update(self, saltar:tuple):
        self.pantalla.blit(cte.easter_fondo, (0,0))
        self.jugador.update(saltar)