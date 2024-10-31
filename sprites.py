import pygame
from constantes import *
import numpy as np
from animacion import Animador

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
        self.animaciones = {}
        self.definirAnimacion()
        self.pararImagen = (8, 0)

    def getIniciodeImagen(self):
        return self.getImagen(8,0)
    
    def getImagen(self, x, y):
        return HojadeSprites.getImagen(self, x, y, 2 * ANCHOCASILLA, 2 * ALTOCASILLA)
    
    def definirAnimacion(self):
        self.animaciones[IZQUIERDA] = Animador(((8, 0), (0, 0), (0, 2), (0, 0)))
        self.animaciones[DERECHA] = Animador(((10, 0), (2, 0), (2, 2), (2, 0)))
        self.animaciones[ARRIBA] = Animador(((10, 2), (6, 0), (6, 2), (6, 0)))
        self.animaciones[ABAJO] = Animador(((8, 2), (4, 0), (4, 2), (4, 0)))

    def actualizar(self, dt):
        if self.entidad.direccion == IZQUIERDA:
            self.entidad.imagen == self.getImagen(*self.animaciones[IZQUIERDA].actualizar(dt))
            self.pararImagen = (8, 0)
        elif self.entidad.direccion == DERECHA:
            self.entidad.imagen == self.getImagen(*self.animaciones[DERECHA].actualizar(dt))
            self.pararImagen = (10, 0)
        elif self.entidad.direccion == ABAJO:
            self.entidad.imagen == self.getImagen(*self.animaciones[ABAJO].actualizar(dt))
            self.pararImagen = (8, 2)
        elif self.entidad.direccion == ARRIBA:
            self.entidad.imagen == self.getImagen(*self.animaciones[ARRIBA].actualizar(dt))
            self.pararImagen = (10, 2)
        elif self.entidad.direccion == DETENER:
            self.entidad.imagen == self.getImagen(*self.pararImagen)

    def reiniciar(self):
        for key in list(self.animaciones.keys()):
            self.animaciones[key].reiniciar()

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
    
    def actualizar(self, dt):
        x = self.x[self.entidad.nombre]
        if self.entidad.modo.actual in [DISPERCION, PERSEGUIR]:
            if self.entidad.direccion == IZQUIERDA:
                 self.entidad.imagen = self.getImagen(x, 8)
            elif self.entidad.direccion == DERECHA:
                  self.entidad.imagen = self.getImagen(x, 10)
            elif self.entidad.direccion == ABAJO:
                  self.entidad.imagen = self.getImagen(x, 6)
            elif self.entidad.direccion == ARRIBA:
                  self.entidad.imagen = self.getImagen(x, 4)
        elif self.entidad.modo.actual == CARGA:
            self.entidad.imagen = self.getImagen(10, 4)
        elif self.entidad.modo.actual == SPAWN:
            if self.entidad.direccion == IZQUIERDA:
                self.entidad.imagen = self.getImagen(8, 8)
            elif self.entidad.direccion == DERECHA:
                self.entidad.imagen = self.getImagen(8, 10)
            elif self.entidad.direccion == ABAJO:
                self.entidad.imagen = self.getImagen(8, 6)
            elif self.entidad.direccion == ARRIBA:
                self.entidad.imagen = self.getImagen(8, 4)

    
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
    

class laberintoSprites(HojadeSprites):
    def __init__(self, archivoLaberinto, archivoRot):
        HojadeSprites.__init__(self)
        self.datos = self.leerArchivoLaberinto(archivoLaberinto)
        self.rotdata = self.leerArchivoLaberinto(archivoRot)

    def getImagen(self, x, y):
            return HojadeSprites.getImagen(self, x, y, ANCHOCASILLA, ALTOCASILLA)
        
    def leerArchivoLaberinto(self, archivoLaberinto):
            return np.loadtxt(archivoLaberinto, dtype='<U1')
        
    def construirFondo(self, fondopantalla, y):
        for fila in list(range(self.datos.shape[0])):
            for col in list(range(self.datos.shape[1])):
                if self.datos[fila][col].isdigit(): #revisar nombres
                        x = int(self.datos[fila][col]) + 12
                        sprite = self.getImagen(x, y)
                        rotval = int(self.rotdata[fila][col])#revisar nombres
                        sprite = self.rotate(sprite, rotval)#revisar nombres
                        fondopantalla.blit(sprite, (col*ANCHOCASILLA, fila*ALTOCASILLA)) #revisar nombres
                elif self.datos[fila][col] == '=':
                        sprite = self.getImagen(10, 8)
                        fondopantalla.blit(sprite, (col*ANCHOCASILLA, fila*ALTOCASILLA))

        return fondopantalla
        
    def rotate(self, sprite, valor): #revisar nombres
        return pygame.transform.rotate(sprite, valor*90)
