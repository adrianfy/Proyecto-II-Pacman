import pygame
from pygame.locals import *
from vector import Vector
from constantes import *
from entidad import Entidad
from estadofantasmas import ModoControlador

class Fantasma (Entidad):
    def __init__(self, nodo, pacman=None):
        Entidad.__init__(self, nodo)
        self.nombre = FANTASMA
        self.puntos = 200
        self.meta = Vector()
        self.metodoDireccion = self.direccionMeta
        self.pacman = pacman
        self.modo = ModoControlador(self)


    def actualizar(self, dt):
        self.modo.actualizar(dt)
        if self.modo.actual is DISPERCION:
            self.disperccion()
        elif self.modo.actual is PERSEGUIR:
            self.perseguir()
        Entidad.actualizar(self, dt)

    def disperccion(self):
        self.meta = Vector()

    def perseguir(self):
        self.meta = self.pacman.posicion

    def iniciarCarga(self):
        self.modo.setModoCarga()
        if self.modo.actual == CARGA:
            self.setVelocidad(50)
            self.metodoDireccion = self.direccionAleatoria

    def modoNormal(self):
        self.setVelocidad(100)
        self.metodoDireccion = self.direccionMeta

    def spawn(self):
        self.meta = self.spawnNode.posicion

    def setSpawnNodo(self, nodo):
        self.spawnNodo = nodo

    def iniciarSpawn(self):
        self.modo.setSpawnMode()
        if self.modo.actual == SPAWN:
            self.setVelocidad(150)
            self.metodoDireccion = self.direccionMeta
            self.spawn()

