import pygame
from vector import Vector
from constantes import *
import numpy as np
import config

# Aqui se hace un ajuste para las imagenes de las bolitas, se reducen o aumentan de tamaño con la finalidad de cambiar
# su imagen para el modo de juego El Tigre.

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

# La clase Bolitas se encarga de crear las bolitas y hereda a bolitas grandes, ambas se encuentran en el mapa

class Bolitas(object):
    # Inicializa las bolitas con una posicion, color, radio, radio de colision y puntos
    def __init__(self, fila, columna):
        self.nombre = BOLITA
        self.posicion = Vector(columna*ANCHOCASILLA, fila*ALTOCASILLA)
        self.color = BLANCO
        self.radio = int(2 * ANCHOCASILLA / 16)
        self.radioColision = int(2*ANCHOCASILLA / 16)
        self.puntos = 10
        self.visibilidad = True
        self.sprite = ranchita
    
    # Actualiza la visibilidad de las bolitas
    def renderizar(self, pantalla):
        if self.visibilidad:
            ajustar = Vector(ANCHOCASILLA, ALTOCASILLA) / 2
            p = self.posicion + ajustar
            # Si el modo de juego es Clasico, pygame se encarga de dibujar un circulo, de lo contrario se renderiza una imagen
            if config.modoDeJuego == "Clasico":
                pygame.draw.circle(pantalla, self.color, p.coordenadaInt(), self.radio)
            else:
                ajuste_x = (nuevo_ancho_ranchita - ANCHOCASILLA) // 2
                ajuste_y = (nuevo_alto_ranchita - ALTOCASILLA) // 2
                posicion_ajustada = (self.posicion.x - ajuste_x, self.posicion.y - ajuste_y)
                pantalla.blit(self.sprite, posicion_ajustada)

# Hereda de la clase Bolitas, se encarga de crear las bolitas grandes que su funcion es diferente
class BolitaGrande(Bolitas):
    # Inicializa las bolitas grandes al igual que la clase bolitas, pero con un radio y puntos diferentes
    def __init__(self, fila, columna):
        Bolitas.__init__(self, fila, columna)
        self.nombre = BOLITAGRANDE
        self.radio = int(8 * ANCHOCASILLA / 16)
        self.puntos = 50
        self.parpadeo = 0.2
        self.timer = 0
        self.sprite = carlsberg

    # Actualiza el parpadeo de las bolitas grandes, clasico del juego de pacman
    def actualizar(self, dt):
        self.timer += dt
        if self.timer >= self.parpadeo:
            self.visibilidad = not self.visibilidad
            self.timer = 0
    
    # Renderiza las bolitas grandes, si el modo de juego es El Tigre, la bolita sera una Carlsberg
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

# La clase GrupoBolitas se encarga de crear un grupo de bolitas y bolitas grandes, ademas de actualizarlas y renderizarlas
class GrupoBolitas(object):
    # Inicializa el grupo de bolitas y bolitas grandes en una lista, ademas de un contador de comidas para saber cuando se acaba el nivel y se llevar el puntaje
    def __init__(self, archivobolita):
        self.listaBolitas = []
        self.bolitaGrande = []
        self.crearListaBolitas(archivobolita)
        self.numComidas = 0
    
    # Actualiza las bolitas y bolitas grandes
    def actualizar(self, dt):
        for bolitaGrande in self.bolitaGrande:
            bolitaGrande.actualizar(dt)

    # Crea una lista de las bolitas y las posiciona segun el txt del laberinto.
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

    # Lee el archivo txt del laberinto
    def leerArchivobolita(self, archivotxt):
        return np.loadtxt(archivotxt, dtype='<U1')
    
    # Verifica si el mapa esta vacio (no hya bolitas)
    def isEmpty(self):
        if len(self.listaBolitas) == 0:
            return True
        return False
    
    # Renderiza las bolitas y bolitas grandes en la pantalla
    def renderizar(self, pantalla):
        for bolita in self.listaBolitas:
            bolita.renderizar(pantalla)
