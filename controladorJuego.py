import pygame
from pygame.locals import *
from constantes import *
from pacman import Pacman
from nodos import GrupoNodos

class ControladorJuego(object):
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMANNOPANTALLA, 0, 32)
        self.fondopantalla = None
        self.reloj = pygame.time.Clock()

    def setFondopantalla(self):
        self.fondopantalla = pygame.surface.Surface(TAMANNOPANTALLA).convert()
        self.fondopantalla.fill(NEGRO)

    def iniciarJuego(self):
        self.setFondopantalla()
        self.nodos = GrupoNodos("laberinto.txt")
        self.pacman = Pacman(self.nodos.getIniciarNodoTemp())
        
    def actualizar(self):
        dt = self.reloj.tick(30) / 1000.0
        self.pacman.actualizar(dt)
        self.verEventos()
        self.renderizar()
    
    def verEventos(self):
        for evento in pygame.event.get():
            if evento.type == QUIT:
                exit()

    def renderizar(self):
        self.pantalla.blit(self.fondopantalla, (0,0))
        self.nodos.renderizar(self.pantalla)
        self.pacman.renderizar(self.pantalla)
        pygame.display.update()

if __name__ == "__main__":
    juego = ControladorJuego()
    juego.iniciarJuego()
    while True:
        juego.actualizar()