import pygame
from vector import Vector
from constantes import *
import numpy as np
import config

factor_reduccion = 0.6  # Reducir al 80% de su tamaño original
nuevo_ancho_ranchita = int(ANCHOCASILLA * factor_reduccion)
nuevo_alto_ranchita = int(ALTOCASILLA * factor_reduccion)

ranchita = pygame.image.load("Recursos/Bolitas/Ranchita.png")
ranchita = pygame.transform.scale(ranchita, (nuevo_ancho_ranchita, nuevo_alto_ranchita))

factor_aumento = 1.6  # Aumentar al 180% de su tamaño original
nuevo_ancho_carlsberg = int(ANCHOCASILLA * factor_aumento)
nuevo_alto_carlsberg = int(ALTOCASILLA * factor_aumento)

carlsberg = pygame.image.load("Recursos/Bolitas/Carlsberg.png")
carlsberg = pygame.transform.scale(carlsberg, (nuevo_ancho_carlsberg, nuevo_alto_carlsberg))

class Bolitas(object):
    def __init__(self, fila, columna):
        self.nombre = BOLITA
        self.posicion = Vector(columna*ANCHOCASILLA, fila*ALTOCASILLA)
        self.color = BLANCO
        self.radio = int(2 * ANCHOCASILLA / 16)
        self.radioColision = int(2*ANCHOCASILLA / 16)
        self.puntos = 10
        self.visibilidad = True
        self.sprite = ranchita

    def renderizar(self, pantalla):
        if self.visibilidad:
            ajustar = Vector(ANCHOCASILLA, ALTOCASILLA) / 2
            p = self.posicion + ajustar
            if config.modoDeJuego == "Clasico":
                pygame.draw.circle(pantalla, self.color, p.coordenadaInt(), self.radio)
            else:
                ajuste_x = (nuevo_ancho_ranchita - ANCHOCASILLA) // 2
                ajuste_y = (nuevo_alto_ranchita - ALTOCASILLA) // 2
                posicion_ajustada = (self.posicion.x - ajuste_x, self.posicion.y - ajuste_y)
                pantalla.blit(self.sprite, posicion_ajustada)

class BolitaGrande(Bolitas):
    def __init__(self, fila, columna):
        Bolitas.__init__(self, fila, columna)
        self.nombre = BOLITAGRANDE
        self.radio = int(8 * ANCHOCASILLA / 16)
        self.puntos = 50
        self.parpadeo = 0.2
        self.timer = 0
        self.sprite = carlsberg

    def actualizar(self, dt):
        self.timer += dt
        if self.timer >= self.parpadeo:
            self.visibilidad = not self.visibilidad
            self.timer = 0
    
    def renderizar(self, pantalla):
        if self.visibilidad:
            ajustar = Vector(ANCHOCASILLA, ALTOCASILLA) / 2
            p = self.posicion + ajustar
            if config.modoDeJuego == "Clasico":
                pygame.draw.circle(pantalla, self.color, p.coordenadaInt(), self.radio)
            else:
                ajuste_x = (nuevo_ancho_carlsberg - ANCHOCASILLA) // 2
                ajuste_y = (nuevo_alto_carlsberg - ALTOCASILLA) // 2
                posicion_ajustada = (self.posicion.x - ajuste_x, self.posicion.y - ajuste_y)
                pantalla.blit(self.sprite, posicion_ajustada)

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
