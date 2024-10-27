import pygame
from pygame.locals import *
from vector import Vector
from constantes import *
from entidad import Entidad

class Fantasma (Entidad):
    def __init__(self, nodo):
        Entidad.__init__(self, nodo)
        self.nombre = FANTASMA
        self.puntos = 200
        self.meta = Vector()
        self.metodoDireccion = self.direccionMeta
        