import pygame
from pygame.locals import *
from vector import Vector
from constantes import *

class Pacman(object):
    def __init__(self):
        self.nombre = PACMAN
        self.posicion = Vector(200, 400)
        self.direcciones = {DETENER:Vector(), ARRIBA:Vector(0,-1), ABAJO:Vector(0,1), IZQUIERDA:Vector(-1,0), DERECHA:Vector(1,0)}
        self.direccion = DETENER
        self.velocidad = 100 * ANCHOCASILLA/16
        self.radio = 10
        self.color = AMARILLO

    def actualizar(self, dt):
        self.posicion += self.direcciones[self.direccion]*self.velocidad*dt
        direccion = self.getTeclaValida()
        self.direccion = direccion

    # Movmimiento de Pacman segun las teclas
    def getTeclaValida(self):
        presionar_Tecla = pygame.key.get_pressed()
        if presionar_Tecla[K_UP] or presionar_Tecla[K_w]:
            return ARRIBA
        if presionar_Tecla[K_DOWN] or presionar_Tecla[K_s]:
            return ABAJO
        if presionar_Tecla[K_LEFT] or presionar_Tecla[K_a]:
            return IZQUIERDA
        if presionar_Tecla[K_RIGHT] or presionar_Tecla[K_d]:
            return DERECHA
        return DETENER
    
    def renderizar(self, pantalla):
        p = self.posicion.coordenadaInt()
        pygame.draw.circle(pantalla, self.color, p, self.radio)