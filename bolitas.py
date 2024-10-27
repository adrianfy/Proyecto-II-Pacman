import pygame
from vector import Vector
from constantes import *
import numpy as np

class Bolitas(object):
    def __init__(self, fila, columna):
        self.nombre = BOLITA
        self.posicion = Vector(columna*ANCHOCASILLA, fila*ALTOCASILLA)
        self.color = BLANCO
        self.radio = int(4*ANCHOCASILLA / 16)
        self.radioColision = int(4*ANCHOCASILLA / 16)
        self.puntos = 10
        self.visbilidad = True

    def renderizar(self, pantalla):
        if self.visbilidad:
            p = self.posicion.coordenadaInt()
            pygame.draw.circle(pantalla, self.color, p, self.radio)

class BolitaGrande(Bolitas):
    def __init__(self, fila, columna):
        Bolitas.__init__(self, fila, columna)
        self.nombre = BOLITAGRANDE
        self.radio = int(8 * ANCHOCASILLA / 16)
        self.puntos = 50
        self.parpadeo = 0.2
        self.timer = 0

    def actualizar(self, dt):
        self.timer += dt
        if self.timer >= self.parpadeo:
            self.visibilidad = not self.visibilidad
            self.timer = 0

class GrupoBolitas(object):
    def __init__(self, archivobolita):
        self.listaBolitas = []
        self.bolitaGrande = []
        self.crearListaBolitas(archivobolita)
        self.numComidas = 0
    
    def actualizar(self, dt):
        for bolitaGrande in self.bolitaGrande:
            bolitaGrande.actualizar(dt)

    def crearListaBolitas(self, archivobolita):
        data = self.leerArchivobolita(archivobolita)
        for fila in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[fila][col] in ['.','+']:
                    self.listaBolitas.append(Bolitas(fila, col))
                elif data[fila][col] in ['P', 'p']:
                    bg = BolitaGrande(fila, col)
                    self.listaBolitas.append(bg)
                    self.bolitaGrande.append(bg)

    def leerArchivobolita(self, archivotxt):
        return np.loadtxt(archivotxt, dtype='<U1')
    
    def isEmpty(self):
        if len(self.listaBolitas) == 0:
            return True
        return False
    
    def renderizar(self, pantalla):
        for bolita in self.listaBolitas:
            bolita.renderizar(pantalla)
