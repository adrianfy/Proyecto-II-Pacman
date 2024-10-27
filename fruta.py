import pygame
from entidad import Entidad
from constantes import *

class Fruta(Entidad):
    def __init__(self, nodo):
        Entidad.__init__(self, nodo)
        self.name = FRUTA
        self.color = VERDE
        self.tiempodevida = 5
        self.timer = 0
        self.desaparecer = False
        self.puntaje = 100
        self.setEntreNodos(DERECHA)

    def actualizar(self, dt):
        self.timer += dt
        if self.timer >= self.tiempodevida:
            self.desaparecer = True