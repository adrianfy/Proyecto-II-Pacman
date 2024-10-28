import pygame
from constantes import *
import numpy as np

ANCHOCASILLABASE = 16
ALTOCASILLABASE = 16

class HojadeSprites(object):
    def __init__(self):
        self.hojaSprite = pygame.image.load("Recursos/Imagenes/pacman.png").convert()
        transcolor = self.hojaSprite.get_at((0,0))
        self.hojaSprite.set_colorkey(transcolor)
        ancho = int(self.hojaSprite.get_width() / ANCHOCASILLABASE * ANCHOCASILLA)
        alto = int(self.hojaSprite.get_height() / ALTOCASILLABASE * ALTOCASILLA)
        self.hojaSprite = pygame.transform.scale(self.hojaSprite, (ancho, alto))

    def getImagen(self, x, y, ancho, alto):
        x *= ANCHOCASILLA
        y *= ALTOCASILLA
        self.hojaSprite.set_clip(pygame.Rect(x,y,ancho, alto))
        return self.hojaSprite.subsurface(self.hojaSprite.get_clip())
    
class ImagendePacman(HojadeSprites):
    def __init__(self, entidad):
        HojadeSprites.__init__(self)
        self.entidad = entidad
        self.entidad.imagen = self.getIniciodeImagen()

    def getIniciodeImagen(self):
        return self.getImagen(8,0)
    
    def getImagen(self, x, y):
        return HojadeSprites.getImagen(self, x, y, 2 * ANCHOCASILLA, 2 * ALTOCASILLA)
    
class ImagendeFantasmas(HojadeSprites):
    def __init__(self, entidad):
        HojadeSprites.__init__(self)
        self.x = {BLINKY: 0, PINKY: 2, INKY: 4, CLYDE: 6}
        self.entidad = entidad
        self.entidad.imagen = self.getIniciodeImagen()
    
    def getIniciodeImagen(self):
        return self.getImagen(self.x[self.entidad.nombre], 4)
    
    def getImagen(self, x, y):
        return HojadeSprites.getImagen(self, x, y, 2* ANCHOCASILLA, 2* ALTOCASILLA)
    
class imagendeFrutas(HojadeSprites):
    def __init__(self, entidad):
        HojadeSprites.__init__(self)
        self.entidad = entidad
        self.entidad.imagen = self.getIniciodeImagen()

    def getIniciodeImagen(self):
        return self.getImagen(16,8)
    
    def getImagen(self, x, y):
        return HojadeSprites.getImagen(self, x, y, 2*ANCHOCASILLA, 2*ALTOCASILLA)
    
class vidasPacman(HojadeSprites):
    def __init__(self, numVidas):
        HojadeSprites.__init__(self)
        self.reiniciarVidas(numVidas)

    def removerImagen(self):
        if len(self.imagenes) > 0:
            self.imagenes.pop(0)

    def reiniciarVidas(self, numVidas):
        self.imagenes = []
        for i in range(numVidas):
            self.imagenes.append(self.getImagen(0,0))

    def getImagen(self, x, y):
        return HojadeSprites.getImagen(self,x ,y, 2*ANCHOCASILLA, 2*ALTOCASILLA)