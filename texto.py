import pygame
from vector import Vector
from constantes import *

class Texto(object):
    def __init__(self, texto, color, x, y, tamanno, tiempo=None, id=None, visbilidad=True):
        self.id = id
        self.texto = texto
        self.color = color
        self.tamanno = tamanno
        self.visbilidad = visbilidad
        self.posicion = Vector(x, y)
        self.timer = 0
        self.tiempodevida = tiempo
        self.tag = None
        self.destruir = False
        self.definirFuente("Recursos/Fuentes/PressStart2P-Regular.ttf")
        self.crearTag()

    def definirFuente(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.tamanno)

    def crearTag(self):
        self.tag = self.font.render(self.texto, 1, self.color)

    def setText(self, nuevotexto):
        self.texto = str(nuevotexto)
        self.crearTag()

    def actualizar(self, dt):
        if self.tiempodevida is not None:
            self.timer += dt
            if self.timer >= self.tiempodevida:
                self.timer = 0
                self.tiempodevida = None
                self.destruir = True

    def renderizar(self, pantalla):
        if self.visbilidad:
            x, y = self.posicion.coordenadaTupla()
            pantalla.blit(self.tag, (x, y))


class GrupoTexto(object):
    def __init__(self):
        self.siguienteid = 10
        self.todotexto = {}
        self.iniciarTexto()
        self.mostrarTexto(INICIOTXT)

    def insertarTexto(self, texto, color, x, y, tamanno, tiempo=None, id=None):
        self.siguienteid += 1
        self.todotexto[self.siguienteid] = Texto(texto, color, x, y, tamanno, tiempo=tiempo, id=id)
        return self.siguienteid

    def eliminarTexto(self, id):
        self.todotexto.pop(id)
        
    def iniciarTexto(self):
        tamanno = ALTOCASILLA
        self.todotexto[PUNTAJETXT] = Texto("0".zfill(8), BLANCO, 0, ALTOCASILLA, tamanno)
        self.todotexto[NIVELTXT] = Texto(str(1).zfill(3), BLANCO, 23*ANCHOCASILLA, ALTOCASILLA, tamanno)
        self.todotexto[INICIOTXT] = Texto("READY!", AMARILLO, 11.25*ANCHOCASILLA, 20*ALTOCASILLA, tamanno, visbilidad=False)
        self.todotexto[PAUSATXT] = Texto("PAUSA!", AMARILLO, 10.625*ANCHOCASILLA, 20*ALTOCASILLA, tamanno, visbilidad=False)
        self.todotexto[GAMEOVERTXT] = Texto("GAMEOVER!", AMARILLO, 10*ANCHOCASILLA, 20*ALTOCASILLA, tamanno, visbilidad=False)
        self.insertarTexto("PUNTAJE", BLANCO, 0, 0, tamanno)
        self.insertarTexto("NIVEL", BLANCO, 23*ANCHOCASILLA, 0, tamanno)

    def actualizar(self, dt):
        for tkey in list(self.todotexto.keys()):
            self.todotexto[tkey].actualizar(dt)
            if self.todotexto[tkey].destruir:
                self.eliminarTexto(tkey)

    def mostrarTexto(self, id):
        self.textoOculto()
        self.todotexto[id].visibilidad = True

    def textoOculto(self):
        self.todotexto[INICIOTXT].visibilidad = False
        self.todotexto[PAUSATXT].visibilidad = False
        self.todotexto[GAMEOVERTXT].visibilidad = False

    def actualizarPuntaje(self, score):
        self.actualizarTexto(PUNTAJETXT, str(score).zfill(8))

    def actualizarNivel(self, level):
        self.actualizarTexto(NIVELTXT, str(level + 1).zfill(3))

    def actualizarTexto(self, id, value):
        if id in self.todotexto.keys():
            self.todotexto[id].setTexto(value)

    def renderizar(self, screen):
        for tkey in list(self.todotexto.keys()):
            self.todotexto[tkey].renderizar(screen)
