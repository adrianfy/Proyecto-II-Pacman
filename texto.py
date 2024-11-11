import pygame
from vector import Vector
from constantes import *

# La clase de texto se encanrga de generar los puntajes o textos dentro del juego. Ejemplo: el puntaje, nivel, pausa, game over, etc.
class Texto(object):
    def __init__(self, texto, color, x, y, tamanno, tiempo=None, id=None, visibilidad=True):
        self.id = id
        self.texto = texto
        self.color = color
        self.tamanno = tamanno
        self.visibilidad = visibilidad
        self.posicion = Vector(x, y)
        self.timer = 0
        self.tiempodevida = tiempo
        self.tag = None
        self.destruir = False
        # Se define la fuente del texto, en este caso usaremos una fuente que se acerca a la clasica de pacman, facilita el cambiar la fuente.
        self.definirFuente("Recursos/Fuentes/PressStart2P-Regular.ttf")
        self.crearTag()

    # Define la fuente del texto
    def definirFuente(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.tamanno)

    # Crea el texto
    def crearTag(self):
        self.tag = self.font.render(self.texto, 1, self.color)

    # Define el texto mediante un string fijo
    def setTexto(self, nuevotexto):
        self.texto = str(nuevotexto)
        self.crearTag()

    # Actualiza el tiempo de vida del texto en algunos casos como el puntaje solo aparecera pro unos segundos y desaparecera
    def actualizar(self, dt):
        if self.tiempodevida is not None:
            self.timer += dt
            if self.timer >= self.tiempodevida:
                self.timer = 0
                self.tiempodevida = None
                self.destruir = True

    # Renderiza el texto
    def renderizar(self, pantalla):
        if self.visibilidad:
            x, y = self.posicion.coordenadaTupla()
            pantalla.blit(self.tag, (x, y))


# La clase GrupoTexto se encarga de crear un grupo de textos, actualizarlos y renderizarlos
class GrupoTexto(object):
    # Inicializa el grupo de textos y crea los textos iniciales
    def __init__(self):
        self.siguienteid = 10
        self.todoeltexto = {}
        self.iniciarTexto()
        self.mostrarTexto(INICIOTXT)

    # Inserta un texto en el grupo de textos
    def insertarTexto(self, texto, color, x, y, tamanno, tiempo=None, id=None):
        self.siguienteid += 1
        self.todoeltexto[self.siguienteid] = Texto(texto, color, x, y, tamanno, tiempo=tiempo, id=id)
        return self.siguienteid

    # Elimina un texto del grupo de textos
    def eliminarTexto(self, id):
        self.todoeltexto.pop(id)
        
    # Inicializa los textos del juegom como el puntaje, nivel, pausa, game over, inicio, de esta forma solo se llamaran en otros lugares del codigo.
    def iniciarTexto(self):
        tamanno = ALTOCASILLA
        self.todoeltexto[PUNTAJETXT] = Texto("0".zfill(8), BLANCO, 0, ALTOCASILLA, tamanno)
        self.todoeltexto[NIVELTXT] = Texto(str(1).zfill(3), BLANCO, 23*ANCHOCASILLA, ALTOCASILLA, tamanno)
        self.todoeltexto[INICIOTXT] = Texto("LISTO?", AMARILLO, 11.25*ANCHOCASILLA, 20*ALTOCASILLA, tamanno, visibilidad=False)
        self.todoeltexto[PAUSATXT] = Texto("PAUSA!", AMARILLO, 10.625*ANCHOCASILLA, 20*ALTOCASILLA, tamanno, visibilidad=False)
        self.todoeltexto[GAMEOVERTXT] = Texto("GAME OVER", AMARILLO, 10*ANCHOCASILLA, 20*ALTOCASILLA, tamanno, visibilidad=False)
        self.insertarTexto("PUNTAJE", BLANCO, 0, 0, tamanno)
        self.insertarTexto("NIVEL", BLANCO, 23*ANCHOCASILLA, 0, tamanno)

    # Actualiza los textos
    def actualizar(self, dt):
        for tkey in list(self.todoeltexto.keys()):
            self.todoeltexto[tkey].actualizar(dt)
            if self.todoeltexto[tkey].destruir:
                self.eliminarTexto(tkey)

    # Muestra un texto en especifico
    def mostrarTexto(self, id):
        self.textoOculto()
        self.todoeltexto[id].visibilidad = True

    # Oculta los textos
    def textoOculto(self):
        self.todoeltexto[INICIOTXT].visibilidad = False
        self.todoeltexto[PAUSATXT].visibilidad = False
        self.todoeltexto[GAMEOVERTXT].visibilidad = False

    # Actualiza el puntaje constantemente
    def actualizarPuntaje(self, score):
        self.actualizarTexto(PUNTAJETXT, str(score).zfill(8))

    # Actualiza el texto del nivel para saber en que nivel esta
    def actualizarNivel(self, level):
        self.actualizarTexto(NIVELTXT, str(level + 1).zfill(3))

    # Actualiza el texto 
    def actualizarTexto(self, id, value):
        if id in self.todoeltexto.keys():
            self.todoeltexto[id].setTexto(value)

    # Renderiza los textos en pantalla 
    def renderizar(self, screen):
        for tkey in list(self.todoeltexto.keys()):
            self.todoeltexto[tkey].renderizar(screen)
