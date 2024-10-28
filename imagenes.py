import pygame
from constantes import *
import numpy as np

ANCHOCASILLABASE = 16
ALTOCASILLABASE = 16

class HojadeImagenes(object):
    def __init__(self):
        self.imagen = pygame.image.load("Recursos/Imagenes/pacman.png").convert()
        transcolor = self.imagen.get_at((0,0))
        self.imagen.set_colorkey(transcolor)
        ancho = int(self.imagen.get_width() / ANCHOCASILLABASE * ANCHOCASILLA)
        alto = int(self.imagen.get_height() / ALTOCASILLABASE * ALTOCASILLA)
        self.imagen = pygame.transform.scale(self.imagen, (ancho, alto))

    def getImagen(self, x, y, ancho, alto):
        x *= ANCHOCASILLA
        y *= ALTOCASILLA
        self.imagen.set_clip(pygame.Rect(x,y,ancho, alto))
        return self.imagen.subsurface(self.imagen.get_clip())
    
class ImagendePacman(HojadeImagenes):
    def __init__(self, entidad):
        HojadeImagenes.__init__(self)
        self.entidad = entidad
        self.entidad.imagen = self.getIniciodeImagen()

    def getIniciodeImagen(self):
        return self.getImagen(8,0)
    
    def getImagen(self, x, y):
        return HojadeImagenes.getImagen(self, x, y, 2 * ANCHOCASILLA, 2 * ALTOCASILLA)
    
class ImagendeFantasmas(HojadeImagenes):
    def __init__(self, entidad):
        HojadeImagenes.__init__(self)
        self.x = {BLINKY: 0, PINKY: 2, INKY: 4, CLYDE: 6}
        self.entidad = entidad
        self.entidad.imagen = self.getIniciodeImagen()
    
    def getIniciodeImagen(self):
        return self.getImagen(self.x[self.entidad.nombre], 4)
    
    def getImagen(self, x, y):
        return HojadeImagenes.getImagen(self, x, y, 2* ANCHOCASILLA, 2* ALTOCASILLA)
    
class imagendeFrutas(HojadeImagenes):
    def __init__(self, entidad):
        HojadeImagenes.__init__(self)
        self.entidad = entidad
        self.entidad.imagen = self.getIniciodeImagen()

    def getIniciodeImagen(self):
        return self.getImagen(16,8)
    
    def getImagen(self, x, y):
        return HojadeImagenes.getImagen(self, x, y, 2*ANCHOCASILLA, 2*ALTOCASILLA)