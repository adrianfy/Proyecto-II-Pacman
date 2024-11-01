import pygame
from pygame.locals import *
from constantes import *
from pacman import Pacman
from nodos import GrupoNodos
from bolitas import GrupoBolitas
from fantasmas import GrupoFantasma
from fruta import Fruta
from pausador import Pausador
from texto import GrupoTexto
from sprites import vidasPacman
from sprites import laberintoSprites

class ControladorJuego(object):
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMANNOPANTALLA, 0, 32)
        self.fondopantalla = None
        self.fondopantalla_normal = None
        self.fondopantalla_flash = None
        self.reloj = pygame.time.Clock()
        self.fruta = None
        self.pausador = Pausador(True)
        self.nivel = 0
        self.vidas = 5
        self.puntaje = 0
        self.grupotexto = GrupoTexto()
        self.vidasPacman = vidasPacman(self.vidas)
        self.flashBG = False
        self.flashtiempo = 0.2
        self.flashtimer = 0
        self.capturarFruta = []

    def restaurarJuego(self):
        self.pausador.pausado = True
        self.pacman.reiniciar()
        self.fantasmas.reiniciar()
        self.fruta = None
        self.grupotexto.mostrarTexto(INICIOTXT)
        self.capturarFruta = []

    def reiniciarNivel(self):
        self.vidas = 5
        self.nivel = 0
        self.pausador.pausado = True
        self.fruta = None
        self.puntaje = 0
        self.grupotexto.actualizarPuntaje(self.puntaje)
        self.grupotexto.actualizarNivel(self.nivel)
        self.grupotexto.actualizarTexto(INICIOTXT)
        self.vidasPacman.reiniciarVidas(self.vidas)
    
    def siguienteNivel(self):
        self.mostrarEntidades()
        self.nivel += 1
        self.pausador.pausado = True
        self.iniciarJuego()
        self.grupotexto.actualizarNivel(self.nivel)

    def setFondopantalla(self):
        self.fondopantalla_normal = pygame.surface.Surface(TAMANNOPANTALLA).convert()
        self.fondopantalla_normal.fill(NEGRO)
        self.fondopantalla_flash = pygame.surface.Surface(TAMANNOPANTALLA).convert()
        self.fondopantalla_flash.fill(NEGRO)
        self.fondopantalla_normal = self.spriteLaberinto.construirFondo(self.fondopantalla_normal, self.nivel % 5)
        self.fondopantalla_flash = self.spriteLaberinto.construirFondo(self.fondopantalla_flash, 5)
        self.flashBG = False
        self.fondopantalla = self.fondopantalla_normal

    def iniciarJuego(self):
        self.spriteLaberinto = laberintoSprites("laberinto.txt", "rotacionLaberinto.txt")
        self.setFondopantalla()
        self.nodos = GrupoNodos("laberinto.txt")
        self.nodos.setPortales((0,17), (27,17))
        casita = self.nodos.crearCasitaFantasmas(11.5, 14)
        self.nodos.connectarNodosCasita(casita, (12,14), IZQUIERDA)
        self.nodos.connectarNodosCasita(casita, (15,14), DERECHA)
        self.pacman = Pacman(self.nodos.getNododesdeCasillas(15,26))
        self.bolitas = GrupoBolitas("laberinto.txt")
        self.fantasmas = GrupoFantasma(self.nodos.getIniciarNodoTemp(), self.pacman)

        self.fantasmas.blinky.setNodoInicial(self.nodos.getNododesdeCasillas(2+11.5, 0+14))
        self.fantasmas.pinky.setNodoInicial(self.nodos.getNododesdeCasillas(2+11.5, 3+14))
        self.fantasmas.inky.setNodoInicial(self.nodos.getNododesdeCasillas(0+11.5, 3+14))
        self.fantasmas.clyde.setNodoInicial(self.nodos.getNododesdeCasillas(4+11.5, 3+14))
        self.fantasmas.setSpawnNodo(self.nodos.getNododesdeCasillas(2+11.5, 3+14))

        self.nodos.denegarAccesoCasita(self.pacman)
        self.nodos.denegarAccesoListaCasita(self.fantasmas)
        self.nodos.denegarAcessoLista(2+11.5, 3+14, IZQUIERDA,self.fantasmas)
        self.nodos.denegarAcessoLista(2+11.5, 3+14, DERECHA,self.fantasmas)
        self.fantasmas.inky.nodoInicial.accesoDenegado(DERECHA,self.fantasmas.inky)
        self.fantasmas.clyde.nodoInicial.accesoDenegado(IZQUIERDA,self.fantasmas.clyde)
        self.nodos.denegarAcessoLista(12, 14, ARRIBA, self.fantasmas)
        self.nodos.denegarAcessoLista(15, 14, ARRIBA, self.fantasmas)
        self.nodos.denegarAcessoLista(12, 26, ARRIBA, self.fantasmas)
        self.nodos.denegarAcessoLista(15, 26, ARRIBA, self.fantasmas)
        

    def actualizar(self):
        dt = self.reloj.tick(30) / 1000.0
        self.grupotexto.actualizar(dt)
        self.bolitas.actualizar(dt)
        if not self.pausador.pausado:
            self.fantasmas.actualizar(dt)
            if self.fruta is not None:
                self.fruta.actualizar(dt)
            self.verEventoBolitas()
            self.verEventoFantasmas()
            self.verEventoFruta()

        if self.pacman.vivo:
            if not self.pausador.pausado:
                self.pacman.actualizar(dt)
        else:
            self.pacman.actualizar(dt)

        if self.flashBG:
            self.flashtimer += dt
            if self.flashtimer >= self.flashtiempo:
                self.flashtimer = 0
                if self.fondopantalla == self.fondopantalla_normal:
                    self.fondopantalla = self.fondopantalla_flash
                else:
                    self.fondopantalla = self.fondopantalla_normal

        despuesdePausar = self.pausador.actualizar(dt)
        if despuesdePausar is not None:
            despuesdePausar()
        self.verEventos()
        self.renderizar()
    
    def actualizarPuntaje(self, puntos):
        self.puntaje += puntos
        self.grupotexto.actualizarPuntaje(self.puntaje)

    def verEventoFantasmas(self):
        for fantasma in self.fantasmas:
            if self.pacman.colisionFantasma(fantasma):
                if fantasma.modo.actual is ASUSTADO:
                    self.pacman.visibilidad = False
                    fantasma.visibilidad = False
                    self.actualizarPuntaje(fantasma.puntos)
                    self.grupotexto.insertarTexto(str(fantasma.puntos), BLANCO, fantasma.posicion.x, fantasma.posicion.y, 8, tiempo=1)
                    self.fantasmas.actualizarPuntos()
                    self.pausador.setPausa(tiempoPausa=1, func=self.mostrarEntidades)
                    fantasma.iniciarSpawn()
                    self.nodos.permitirAccesoCasita(fantasma)
                elif fantasma.modo.actual is not SPAWN:
                    if self.pacman.vivo:
                        self.vidas -= 1
                        self.vidasPacman.removerImagen()
                        self.pacman.muerto()
                        self.fantasmas.esconderse()
                        if self.vidas <= 0:
                            self.grupotexto.mostrarTexto(GAMEOVERTXT)
                            self.pausador.setPausa(tiempoPausa=3, func=self.reiniciarNivel)
                        else:
                            self.pausador.setPausa(tiempoPausa=3, func=self.restaurarJuego)

    def verEventoFruta(self):
        if self.bolitas.numComidas == 50 or self.bolitas.numComidas == 140:
            if self.fruta is None:
                self.fruta = Fruta(self.nodos.getNododesdeCasillas(9,20), self.nivel)
        if self.fruta is not None:
            if self.pacman.verColision(self.fruta):
                self.actualizarPuntaje(self.fruta.puntaje)
                self.grupotexto.insertarTexto(str(self.fruta.puntaje), BLANCO, self.fruta.posicion.x, self.fruta.posicion.y, 8, tiempo=1)
                capturarFruta = False
                for fruta in self.capturarFruta:
                    if fruta.get_recompensa() == self.fruta.imagen.get_recompensa():
                        capturarFruta = True
                        break
                if not capturarFruta:
                    self.capturarFruta.append(self.fruta.imagen)
                self.fruta = None
            elif self.fruta.desaparecer:
                self.fruta = None

    def verEventoBolitas(self):
        bolitas = self.pacman.bolitasComidas(self.bolitas.listaBolitas)
        if bolitas:
            self.bolitas.numComidas += 1
            self.actualizarPuntaje(bolitas.puntos)
            if self.bolitas.numComidas == 30:
                self.fantasmas.inky.nodoInicial.accesoPermitido(DERECHA, self.fantasmas.inky)
            if self.bolitas.numComidas == 70:
                self.fantasmas.clyde.nodoInicial.accesoPermitido(IZQUIERDA, self.fantasmas.clyde)
            self.bolitas.listaBolitas.remove(bolitas)
            if bolitas.nombre == BOLITAGRANDE:
                self.fantasmas.iniciarSusto()
            if self.bolitas.isEmpty():
                self.flashBG = True
                self.esconderEntidades()
                self.pausador.setPausa(tiempoPausa=3, func=self.siguienteNivel)

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
                    if self.pacman.vivo:
                        self.pausador.setPausa(jugadorPauso=True)
                        if not self.pausador.pausado:
                         self.grupotexto.textoOculto()
                         self.mostrarEntidades()
                        else:
                            self.grupotexto.mostrarTexto(PAUSATXT)
                            self.esconderEntidades()

    def renderizar(self):
        self.pantalla.blit(self.fondopantalla, (0,0))
        self.bolitas.renderizar(self.pantalla)
        if self.fruta is not None:
            self.fruta.renderizar(self.pantalla)
        self.pacman.renderizar(self.pantalla)
        self.fantasmas.renderizar(self.pantalla)
        self.grupotexto.renderizar(self.pantalla)

        for i in range(len(self.vidasPacman.imagenes)):
            x = self.vidasPacman.imagenes[i].get_width() * i
            y = ALTOPANTALLA - self.vidasPacman.imagenes[i].get_height()
            self.pantalla.blit(self.vidasPacman.imagenes[i], (x, y))

        for i in range(len(self.capturarFruta)):
            x = ANCHOPANTALLA - self.capturarFruta1[i].get_ancho() * (i+1)
            y = ALTOPANTALLA - self.capturarFruta[i].get_alto()
            self.pantalla.blit(self.capturarFruta[i], (x, y))

        pygame.display.update()

# if __name__ == "__main__":
#     juego = ControladorJuego()
#     juego.iniciarJuego()
#     while True:
#         juego.actualizar()