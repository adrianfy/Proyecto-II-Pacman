import pygame
from pygame.locals import *
from constantes import *
from pacman import Pacman
from nodos import GrupoNodos
from bolitas import GrupoBolitas
from fantasmas import GrupoFantasma
from fruta import Fruta
from pausa import Pausa

class ControladorJuego(object):
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMANNOPANTALLA, 0, 32)
        self.fondopantalla = None
        self.reloj = pygame.time.Clock()
        self.fruta = None
        self.pausa = Pausa(True)
        self.nivel = 0
    
    def siguienteNivel(self):
        self.mostrarEntidades()
        self.nivel += 1
        self.pausa.pausa = True
        self.iniciarJuego()

    def setFondopantalla(self):
        self.fondopantalla = pygame.surface.Surface(TAMANNOPANTALLA).convert()
        self.fondopantalla.fill(NEGRO)

    def iniciarJuego(self):
        self.setFondopantalla()
        self.nodos = GrupoNodos("laberinto.txt")
        self.nodos.setPortales((0,17),(27,17))
        self.pacman = Pacman(self.nodos.getNododesdeCasillas(15,26))
        self.bolitas = GrupoBolitas("laberinto.txt")
        self.fantasmas = GrupoFantasma(self.nodos.getIniciarNodoTemp(), self.pacman)
        self.fantasmas.blinky.setNodoInicial(self.nodos.getNododesdeCasillas(2+11.5, 0+14))
        self.fantasmas.pinky.setNodoInicial(self.nodos.getNododesdeCasillas(2+11.5, 3+14))
        self.fantasmas.inky.setNodoInicial(self.nodos.getNododesdeCasillas(0+11.5, 3+14))
        self.fantasmas.clyde.setNodoInicial(self.nodos.getNododesdeCasillas(4+11.5, 3+14))
        self.fantasmas.setSpawnNodo(self.nodos.getNododesdeCasillas(2+11.5, 3+14))

    def actualizar(self):
        dt = self.reloj.tick(30) / 1000.0
        self.pacman.actualizar(dt)
        self.bolitas.actualizar(dt)
        if not self.pausa.pausa:
            self.fantasmas.actualizar(dt)
            if self.fruta is not None:
                self.fruta.actualizar(dt)
            self.verEventoBolitas()
            self.verEventoFantasmas()
            self.verEventoFruta()
        despuesdePausar = self.pausa.actualizar(dt)
        if despuesdePausar is not None:
            despuesdePausar()
        self.verEventos()
        self.renderizar()
    
    def verEventoFantasmas(self):
        for fantasma in self.fantasmas:
            if self.pacman.colisionFantasma(fantasma):
                if fantasma.modo.actual is CARGA:
                    fantasma.iniciarSpawn()

    def verEventoFruta(self):
        if self.bolitas.numComidas == 50 or self.bolitas.numComidas == 100:
            if self.fruta is None:
                self.fruta = Fruta(self.nodos.getNododesdeCasillas(9,20))
        if self.fruta is not None:
            if self.pacman.verColision(self.fruta):
                self.fruta = None
            elif self.fruta.desaparecer:
                self.fruta = None

    def verEventoBolitas(self):
        bolitas = self.pacman.bolitasComidas(self.bolitas.listaBolitas)
        if bolitas:
            self.bolitas.numComidas += 1
            self.bolitas.listaBolitas.remove(bolitas)
            if bolitas.nombre == BOLITAGRANDE:
                self.fantasmas.iniciarSusto()
            if self.bolitas.isEmpty():
                self.esconderEntidades()
                self.pausa.setPausa(tiempoPausa=3, func=self.siguienteNivel)

    def mostrarEntidades(self):
        self.pacman.visibilidad = True
        self.fantasmas.mostrarse()

    def esconderEntidades(self):
        self.pacman.visibilidad = False
        self.fantasmas.esconderse()

    def verEventos(self):
        for evento in pygame.event.get():
            if evento.type == QUIT:
                exit()
            elif evento.type == KEYDOWN:
                if evento.key == K_SPACE:
                    self.pausa.setPausa(jugadorPauso=True)
                    if not self.pausa.pausa:
                        self.mostrarEntidades()
                    else:
                        self.esconderEntidades()

    def renderizar(self):
        self.pantalla.blit(self.fondopantalla, (0,0))
        self.nodos.renderizar(self.pantalla)
        self.bolitas.renderizar(self.pantalla)
        self.pacman.renderizar(self.pantalla)
        self.fantasmas.renderizar(self.pantalla)
        pygame.display.update()

if __name__ == "__main__":
    juego = ControladorJuego()
    juego.iniciarJuego()
    while True:
        juego.actualizar()