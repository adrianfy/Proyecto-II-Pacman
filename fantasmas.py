import pygame
from pygame.locals import *
from vector import Vector
from constantes import *
from entidad import Entidad
from estadofantasmas import ModoControlador
from imagenes import ImagendeFantasmas

class Fantasma (Entidad):
    def __init__(self, nodo, pacman=None, blinky=None):
        Entidad.__init__(self, nodo)
        self.nombre = FANTASMA
        self.puntos = 200
        self.meta = Vector()
        self.metodoDireccion = self.direccionMeta
        self.pacman = pacman
        self.modo = ModoControlador(self)
        self.blinky = blinky
        self.nodoCasita = nodo

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

    def iniciarSusto(self):
        self.modo.setModoCarga()
        if self.modo.actual == CARGA:
            self.setVelocidad(50)
            self.metodoDireccion = self.direccionAleatoria

    def modoNormal(self):
        self.setVelocidad(100)
        self.metodoDireccion = self.direccionMeta
        self.nodoCasita.accesoDenegado(ABAJO, self)

    def spawn(self):
        self.meta = self.spawnNodo.posicion

    def setSpawnNodo(self, nodo):
        self.spawnNodo = nodo

    def iniciarSpawn(self):
        self.modo.setSpawnMode()
        if self.modo.actual == SPAWN:
            self.setVelocidad(150)
            self.metodoDireccion = self.direccionMeta
            self.spawn()

class Blinky(Fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        Fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre = BLINKY
        self.color = ROJO
        self.imagen = ImagendeFantasmas(self)

class Pinky(Fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        Fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre = PINKY
        self.color = ROSADO
        self.imagen = ImagendeFantasmas(self)

    def disperccion(self):
        self.meta = Vector(ANCHOCASILLA*COLUMNA, 0)

    def perseguir(self):
        self.meta = self.pacman.posicion + self.pacman.direcciones[self.pacman.direccion] * ANCHOCASILLA * 4

class Inky(Fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        Fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre = INKY
        self.color = CYAN
        self.imagen = ImagendeFantasmas(self)
    
    def disperccion(self):
        self.meta = Vector(ANCHOCASILLA * COLUMNA, ALTOCASILLA * FILA)

    def perseguir(self):
        vec1 = self.pacman.posicion + self.pacman.direcciones[self.pacman.direccion] * ANCHOCASILLA * 4
        vec2 = (vec1 - self.blinky.posicion) * 2
        self.meta = self.blinky.posicion + vec2
    
class Clyde(Fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        Fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre = CLYDE
        self.color = NARANJA
        self.imagen = ImagendeFantasmas(self)

    def disperccion(self):
        self.goal = Vector(0, ANCHOCASILLA * FILA)

    def perseguir(self):
        d = self.pacman.posicion - self.posicion
        ds = d.magnitudCuadrados()
        if ds <= (ANCHOCASILLA * 8) **2:
            self.disperccion()
        else:
            self.meta = self.pacman.posicion + self.pacman.direcciones[self.pacman.direccion] * ANCHOCASILLA * 4

class GrupoFantasma(object):
    def __init__(self, nodo, pacman):
        self.blinky = Blinky(nodo, pacman)
        self.pinky = Pinky(nodo, pacman)
        self.inky = Inky(nodo, pacman)
        self.clyde = Clyde(nodo, pacman)
        self.fantasmas = [self.blinky, self.pinky, self.inky, self.clyde]
    
    def __iter__(self):
        return iter(self.fantasmas)

    def actualizar(self, dt):
        for fantasma in self:
            fantasma.actualizar(dt)

    def iniciarSusto(self):
        for fantasma in self:
            fantasma.iniciarSusto()
        self.reiniciarPuntos()

    def setSpawnNodo(self, nodo):
        for fantasma in self:
            fantasma.setSpawnNodo(nodo)

    def actualizarPuntos(self):
        for fantasma in self:
            fantasma.puntos *= 2

    def reiniciarPuntos(self):
        for fantasma in self:
            fantasma.puntos = 200

    def reiniciar(self):
        Entidad.reiniciar(self)
        self.puntos = 200
        self.metodoDireccion = self.direccionMeta

    def esconderse(self):
        for fantasma in self:
            fantasma.visibilidad = False
    
    def mostrarse(self):
        for fantasma in self:
            fantasma.visibilidad = True

    def renderizar(self, pantalla):
        for fantasma in self:
            fantasma.renderizar(pantalla)

