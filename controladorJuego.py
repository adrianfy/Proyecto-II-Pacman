import pygame
from pygame.locals import *
from constantes import *
from pacman import Pacman
from nodos import GrupoNodos
from bolitas import GrupoBolitas, Bolitas, BolitaGrande
from fantasmas import GrupoFantasma
from fruta import Fruta
from pausador import Pausador
from texto import GrupoTexto
from sprites import vidasPacman
from sprites import laberintoSprites
import config
import json

from vector import Vector
#import pickle

#Esta clase se encarga de controlar el juego, es decir, de actualizar y renderizar las entidades del juego
class ControladorJuego(object):
    def __init__(self, modo_juego="Clasico"):
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
        self.nodoFruta = None
        self.modo_juego = modo_juego
        self.menu_pausa = False 

    def restaurarJuego(self):#Restaura el juego despues de que pacman muere
        self.pausador.pausado = True
        self.pacman.reiniciar()
        self.fantasmas.reiniciar()
        self.fruta = None
        self.grupotexto.mostrarTexto(INICIOTXT)

    def reiniciarNivel(self):#Reinicia el nivel despues de que pacman pierde todas sus vidas
        self.vidas = 5
        self.nivel = 0
        self.pausador.pausado = True
        self.fruta = None
        self.iniciarJuego()
        self.puntaje = 0
        self.grupotexto.actualizarPuntaje(self.puntaje)
        self.grupotexto.actualizarNivel(self.nivel)
        self.grupotexto.mostrarTexto(INICIOTXT)
        self.vidasPacman.reiniciarVidas(self.vidas)
        self.capturarFruta = []
    
    def siguienteNivel(self):#Pasa al siguiente nivel
        self.mostrarEntidades()
        self.nivel += 1
        self.pausador.pausado = True
        self.iniciarJuego()
        self.fantasmas.inky.velocidad += 1
        self.fantasmas.clyde.velocidad += 1
        self.fantasmas.blinky.velocidad += 1
        self.fantasmas.pinky.velocidad += 1
        self.grupotexto.actualizarNivel(self.nivel)

    def setFondopantalla(self):#Crea el fondo del juego
        self.fondopantalla_normal = pygame.surface.Surface(TAMANNOPANTALLA).convert()
        self.fondopantalla_normal.fill(NEGRO)
        self.fondopantalla_flash = pygame.surface.Surface(TAMANNOPANTALLA).convert()
        self.fondopantalla_flash.fill(NEGRO)
        self.fondopantalla_normal = self.spriteLaberinto.construirFondo(self.fondopantalla_normal, self.nivel % 5)
        self.fondopantalla_flash = self.spriteLaberinto.construirFondo(self.fondopantalla_flash, 5)
        self.flashBG = False
        self.fondopantalla = self.fondopantalla_normal

    def iniciarJuego(self):#Inicia el juego con un laberinto de nodos para buscar caminos de fantasmas
        if config.modoDeJuego == "El Tigre":
            pygame.mixer.music.load("Recursos/Audio/Adiccion [Insturmental].mp3")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        self.spriteLaberinto = laberintoSprites("laberinto.txt", "rotacionLaberinto.txt")
        self.setFondopantalla()
        self.nodos = GrupoNodos("laberinto.txt")
        self.nodos.setPortales((0,17), (27,17))
        casita = self.nodos.crearCasitaFantasmas(11.5, 14)
        self.nodos.connectarNodosCasita(casita, (12,14), IZQUIERDA)
        self.nodos.connectarNodosCasita(casita, (15,14), DERECHA)

        self.pacman = Pacman(self.nodos.getNododesdeCasillas(15,26))
        
        recuperarPartida = self.cargarPartida()
        if recuperarPartida is not None:
            self.bolitas = recuperarPartida
            self.grupotexto.actualizarPuntaje(self.puntaje)
            self.grupotexto.actualizarNivel(self.nivel)
            self.bolitas.actualizar(0)
        else:
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
        

    def actualizar(self):#Actualiza el juego y sus entidades
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
        self.renderizar(self.vidas)
    
    def actualizarPuntaje(self, puntos):
        self.puntaje += puntos
        self.grupotexto.actualizarPuntaje(self.puntaje)

    def verEventoFantasmas(self):#Verifica si pacman colisiona con un fantasma
        for fantasma in self.fantasmas:
            if self.pacman.colisionFantasma(fantasma):
                if fantasma.modo.actual is ASUSTADO:
                    self.pacman.visibilidad = False
                    fantasma.visibilidad = False
                    self.actualizarPuntaje(fantasma.puntos)
                    self.grupotexto.insertarTexto(str(fantasma.puntos), BLANCO, fantasma.posicion.x, fantasma.posicion.y, 8, tiempo=1)
                    pygame.mixer.Sound("Recursos/Audio/comerFantasma.wav").play()
                    self.fantasmas.actualizarPuntos()
                    self.pausador.setPausa(tiempoPausa=1, func=self.mostrarEntidades)
                    fantasma.iniciarSpawn()
                    self.nodos.permitirAccesoCasita(fantasma)
                elif fantasma.modo.actual is not SPAWN:
                    if self.pacman.vivo:
                        self.vidas -= 1
                        self.vidasPacman.removerImagen()
                        self.pacman.muerto()
                        pygame.mixer.Sound("Recursos/Audio/muerte.mp3").play()  if config.modoDeJuego == "Clasico" else pygame.mixer.Sound("Recursos/Audio/muerteMondevil.mp3").play()
                        self.fantasmas.esconderse()
                        if self.vidas <= 0:
                            self.grupotexto.mostrarTexto(GAMEOVERTXT)
                            self.pausador.setPausa(tiempoPausa=3, func=self.reiniciarNivel)
                        else:
                            self.pausador.setPausa(tiempoPausa=3, func=self.restaurarJuego)

    def verEventoFruta(self):#Verifica si pacman se come las frutas
        if self.bolitas.numComidas == 50 or self.bolitas.numComidas == 140:
            if self.fruta is None:
                self.fruta = Fruta(self.nodos.getNododesdeCasillas(9,20), self.nivel)
        if self.fruta is not None:
            if self.pacman.verColision(self.fruta):
                self.actualizarPuntaje(self.fruta.puntaje)
                pygame.mixer.Sound("Recursos/Audio/comerFruta.wav").play() if config.modoDeJuego == "Clasico" else pygame.mixer.Sound("Recursos/Audio/soda.mp3").play()
                self.grupotexto.insertarTexto(str(self.fruta.puntaje), BLANCO, self.fruta.posicion.x, self.fruta.posicion.y, 8, tiempo=1)
                capturarFruta = False
                for fruta in self.capturarFruta:
                    if fruta.get_offset() == self.fruta.imagen.get_offset():
                        capturarFruta = True
                        break
                if not capturarFruta:
                    self.capturarFruta.append(self.fruta.imagen)
                self.fruta = None
            elif self.fruta.desaparecer:
                self.fruta = None

    def verEventoBolitas(self):#Verifica si pacman se come una bolita
        bolitas = self.pacman.bolitasComidas(self.bolitas.listaBolitas)
        if bolitas:
            self.bolitas.numComidas += 1
            self.actualizarPuntaje(bolitas.puntos)
            pygame.mixer.Sound("Recursos/Audio/comer.mp3").play()
            if self.bolitas.numComidas == 30:
                self.fantasmas.inky.nodoInicial.accesoPermitido(DERECHA, self.fantasmas.inky)
            if self.bolitas.numComidas == 70:
                self.fantasmas.clyde.nodoInicial.accesoPermitido(IZQUIERDA, self.fantasmas.clyde)
            self.bolitas.listaBolitas.remove(bolitas)
            if bolitas.nombre == BOLITAGRANDE:
                if config.modoDeJuego == "El Tigre":
                    pygame.mixer.Sound("Recursos/Audio/BolitaGrande.mp3").stop() 
                    pygame.mixer.Sound("Recursos/Audio/BolitaGrande.mp3").play() 
                self.fantasmas.iniciarSusto()
            if self.bolitas.isEmpty():
                if config.modoDeJuego == "Clasico":
                    pygame.mixer.Sound("Recursos/Audio/pacman_intermission.wav").play()
                else:
                    pygame.mixer.Sound("Recursos/Audio/Adiccion[Ganar].mp3").play()
                self.flashBG = True
                self.esconderEntidades()
                self.pausador.setPausa(tiempoPausa=3, func=self.siguienteNivel)

    def mostrarEntidades(self):#Muestra las entidades del juego
        self.pacman.visibilidad = True
        self.fantasmas.mostrarse()

    def esconderEntidades(self):#Esconde las entidades del juego
        self.pacman.visibilidad = False
        self.fantasmas.esconderse()

    def verEventos(self):#Verifica los eventos del juego
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.sound.stop()
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
                           # self.esconderEntidades()
                if evento.key == K_g:
                    self.guardarPartida()

    # Las funciones de guardar y cargar en multiplas clases fueron obtenidas desde Github Copilot con
    # modificaciones para el funcionamiento correcto del programa
    def guardarPartida(self):
        my_dict = {
            "puntaje" : self.puntaje,
            "nivel" : self.nivel,
            "vidas" : self.vidas,
            "bolitas" : {"bolitasPeque" : self.bolitas.listaBolitas, "bolitasGrandes" : self.bolitas.bolitaGrande, "numComidas" : self.bolitas.numComidas},

        }
        with open("PartidaPacman.json", "w") as file:
            json.dump(my_dict, file, indent=4, cls=CustomEncoder)

    def cargarPartida(self):
        try:
            with open("PartidaPacman.json", "r") as file:
                data = json.load(file)
                self.puntaje = data["puntaje"]
                self.nivel = data["nivel"]
                self.vidas = data["vidas"]
                return GrupoBolitas.from_dict(data["bolitas"])
        except: 
            return None


    def renderizar(self, vidas=None):
        self.pantalla.blit(self.fondopantalla, (0,0))
        self.bolitas.renderizar(self.pantalla)
        if self.fruta is not None:
            self.fruta.renderizar(self.pantalla)
        self.pacman.renderizar(self.pantalla)
        self.fantasmas.renderizar(self.pantalla)
        self.grupotexto.renderizar(self.pantalla)

        vidasActuales = len(self.vidasPacman.imagenes) if vidas is None else vidas
        for i in range(vidasActuales):
            x = self.vidasPacman.imagenes[i].get_width() * i
            y = ALTOPANTALLA - self.vidasPacman.imagenes[i].get_height()
            self.pantalla.blit(self.vidasPacman.imagenes[i], (x, y))

        for i in range(len(self.capturarFruta)):
            x = ANCHOPANTALLA - self.capturarFruta[i].get_width() * (i+1)
            y = ALTOPANTALLA - self.capturarFruta[i].get_height()
            self.pantalla.blit(self.capturarFruta[i], (x, y))

        pygame.display.update()

# Se recurrio a ayuda externa como Github Copilot para la creacion de la clase CustomEncoder, solo se modifico para el
# funcionamiento correcto del programa
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (GrupoBolitas, Bolitas, BolitaGrande, Vector)):
            return obj.to_dict()
        return super().default(obj)

