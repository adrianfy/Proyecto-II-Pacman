import pygame
from pygame.locals import *
from vector import Vector
from constantes import *
from entidad import Entidad

class Pacman(Entidad):
    def __init__(self, nodo):
        Entidad.__init__(self,nodo)
        self.nombre = PACMAN
        self.direcciones = {DETENER:Vector(), ARRIBA:Vector(0,-1), ABAJO:Vector(0,1), IZQUIERDA:Vector(-1,0), DERECHA:Vector(1,0)}
        self.direccion = DETENER
        self.velocidad = 100 * ANCHOCASILLA/16
        self.radio = 10
        self.color = AMARILLO
        self.direccion = IZQUIERDA
        self.nodo = nodo
        #self.setPosicion()
        self.objetivo = nodo
        self.radioColision = 5
        self.setEntreNodos(IZQUIERDA)

    def setPosicion(self):
        self.posicion = self.nodo.posicion.copia()

    def actualizar(self, dt):
        self.posicion += self.direcciones[self.direccion]*self.velocidad*dt
        direccion = self.getTeclaValida()
        if self.objetivoRebasado():
            if self.nodo.definirConexion[PORTAL] is not None:
                self.nodo = self.nodo.definirConexion[PORTAL]
            self.nodo = self.objetivo
            self.objetivo = self.getNuevoObjetivo(direccion)
            if self.objetivo is not self.nodo:
                self.direccion = direccion
            else:
                self.objetivo = self.getNuevoObjetivo(self.direccion)
            if self.objetivo is self.nodo:
                self.direccion = DETENER
            self.setPosicion()
        else:
            if self.direccionOpuesta(direccion):
                self.direccionReversa()

    def validarDirreccion(self, direccion):
        if direccion is not DETENER:
            if self.nodo.definirConexion[direccion] is not None:
                return True
        return False

    def getNuevoObjetivo(self, direccion):
        if self.validarDirreccion(direccion):
            return self.nodo.definirConexion[direccion]
        return self.nodo
    
    # Movmimiento de Pacman segun las teclas
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
    
    def objetivoRebasado(self):
        if self.objetivo is not None:
            vec1 = self.objetivo.posicion - self.nodo.posicion
            vec2 = self.posicion - self.nodo.posicion
            nodoAobjetivo = vec1.magnitudCuadrados()
            nodoAself = vec2.magnitudCuadrados()
            return nodoAself >= nodoAobjetivo
        return False
    
    def direccionReversa(self):
        self.direccion *= -1
        temp = self.nodo
        self.nodo = self.objetivo
        self.objetivo = temp

    def direccionOpuesta(self, direccion):
        if direccion is not DETENER:
            if direccion == self.direccion * -1:
                return True
        return False
    
    def bolitasComidas(self,listaBolitas):
        for bolitas in listaBolitas:
            d = self.posicion - bolitas.posicion
            dCuadrado = d.magnitudCuadrados()
            rCuadrado = (bolitas.radio+self.radioColision)**2
            if dCuadrado <= rCuadrado:
                return bolitas
        return None

    def renderizar(self, pantalla):
        p = self.posicion.coordenadaInt()
        pygame.draw.circle(pantalla, self.color, p, self.radio)