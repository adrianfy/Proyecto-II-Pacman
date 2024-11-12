import pygame
from pygame.locals import *
from vector import Vector
from constantes import *
from entidad import Entidad
from sprites import ImagendePacman

# Clase Pacman, se encarga de crear al personaje principal del juego, una bolita amarilla que come bolitas
class Pacman(Entidad):
    # Inicializa a Pacman con un nodo
    def __init__(self, nodo):
        Entidad.__init__(self,nodo)
        self.nombre = PACMAN
        self.color = AMARILLO
        self.direccion = IZQUIERDA
        self.setEntreNodos(IZQUIERDA)
        self.vivo = True
        self.sprites = ImagendePacman(self)

    # Reinicia a Pacman
    def reiniciar(self):
        Entidad.reiniciar(self)
        self.direccion = IZQUIERDA
        self.setEntreNodos(IZQUIERDA)
        self.vivo = True
        self.imagen = self.sprites.getIniciodeImagen()
        self.sprites.reiniciar()

    # Si un fantasma toca a pacman, este se detiene y muere
    def muerto(self):
        self.vivo = False
        self.direccion = DETENER

    #def setPosicion(self):
      #  self.posicion = self.nodo.posicion.copia()

    # Actualiza a el ciclo de Pacman tanto de movimiento como de animacion, posicion y colisiones
    def actualizar(self, dt):
        self.sprites.actualizar(dt)
        self.posicion += self.direcciones[self.direccion]*self.velocidad*dt
        direccion = self.getTeclaValida()
        if self.objetivoRebasado():
            self.nodo = self.objetivo
            if self.nodo.definirConexion[PORTAL] is not None:
                self.nodo = self.nodo.definirConexion[PORTAL]
            self.objetivo = self.objetivoNuevo(direccion)
            if self.objetivo is not self.nodo:
                self.direccion = direccion
            else:
                self.objetivo = self.objetivoNuevo(self.direccion)
            if self.objetivo is self.nodo:
                self.direccion = DETENER
            self.setPosicion()
        else:
            if self.direccionOpuesta(direccion):
                self.direccionInversa()
    
    # Movmimiento de Pacman segun las teclas, se agrego la opcion de jugar con las flechas o con WASD
    def getTeclaValida(self):
        presionar_Tecla = pygame.key.get_pressed()
        if presionar_Tecla[K_UP] or presionar_Tecla[K_w]:
            return ARRIBA
        if presionar_Tecla[K_DOWN] or presionar_Tecla[K_s]:
            return ABAJO
        if presionar_Tecla[K_LEFT] or presionar_Tecla[K_a]:
            return IZQUIERDA
        if presionar_Tecla[K_RIGHT] or presionar_Tecla[K_d]:
            return DERECHA
        return DETENER
    
    # Si Pacman colisiona con una bolita, esta desaparece y suma puntos
    def bolitasComidas(self,listaBolitas):
        for bolitas in listaBolitas:
            if self.verColision(bolitas):
                return bolitas
        return None
    
    # Revisa la colision con fantasmas
    def colisionFantasma(self, fantasma):
        return self.verColision(fantasma)
    
    # Revisa las posibles colisiones, esta es en funcion a los radiso de los objetos ya que la mayoria se definen como circulos.
    def verColision(self, otro):
        d = self.posicion - otro.posicion
        dCuadrado = d.magnitudCuadrados()
        rCuadrado = (self.radioColision + otro.radioColision)**2
        if dCuadrado <= rCuadrado:
            return True
        return False
