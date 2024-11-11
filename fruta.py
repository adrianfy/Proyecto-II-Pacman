import pygame
from entidad import Entidad
from constantes import *
from sprites import imagendeFrutas

# La clase Fruta se encarga de crear las frutas que aparecen en el mapa
class Fruta(Entidad):
    # Inicializa la fruta con un nodo y un nivel, tienen su propio sprite y puntaje
    def __init__(self, nodo, nivel = 0):
        Entidad.__init__(self, nodo)
        self.nombre = FRUTA
        self.color = VERDE
        self.tiempodevida = 5
        self.timer = 0
        self.desaparecer = False
        self.puntaje = 100 + nivel*20
        self.setEntreNodos(DERECHA)
        self.sprites = imagendeFrutas(self, nivel)

    # Actualiza la fruta
    def actualizar(self, dt):
        self.timer += dt
        if self.timer >= self.tiempodevida:
            self.desaparecer = True