import pygame
from pygame.locals import *
from vector import Vector
from constantes import *
from random import randint

class Entidad(object):
    def __init__(self, nodo):
        self.nombre = None
        self.direcciones = {ARRIBA:Vector(0, -1),ABAJO:Vector(0,1), IZQUIERDA:Vector(-1, 0), DERECHA:Vector(1, 0), DETENER:Vector()}
        self.direcion = DETENER
        self.setVelocidad(100)
        self.radio = 10
        self.radioColision = 5
        self.color = BLANCO
        self.nodo = nodo
        self.setPosicion()
        self.objetivo = nodo
        self.visibilidad = True
        self.portalDesactivado = False

    def setPosicion(self):
        self.posicion = self.nodo.posicion.copy()

    def direccionValida(self, direccion):
        if direccion is not DETENER:
            if self.nodo.definirConexion[direccion] is not None:
                return True
            return False

    def objetivoNuevo(self, direccion):
        if self.direccionValida(direccion):
            return self.nodo.definirConexion[direccion]
        return self.nodo

    def objetivoRebasado(self):
        if self.objetivo is not None:
            vec1 = self.objetivo.posicion - self.nodo.posicion
            vec2 = self.posicion - self.nodo.posicion
            nodoObjetivo = vec1.magnitudCuadrados()
            nodoSelf = vec2.magnitudCuadrados()
            return nodoSelf >= nodoObjetivo
        return False

    def direccionInversa(self):
        self.direcion *= -1
        temp = self.nodo
        self.nodo = self.objetivo
        self.objetivo = temp

    def direccionOpuesta(self, direccion):
        if direccion is not DETENER:
            if direccion == self.direcion * -1:
                return True
        return False

    def setVelocidad(self, velocidad):
        self.velocidad = velocidad * ANCHOCASILLA / 16

    def renderizar(self, pantalla):
        if self.visible:
            p = self.posicion.asInt()
            pygame.draw.circle(pantalla, self.color, p, self.radio)



    def actualizacion(self, dt):
        self.posicion += self.direcciones[self.direccion]*self.velocidad*dt

        if self.objetivoRebasado():
            self.nodo = self.objetivo
            direcciones = self.direccionValida()
            direccion = self.direccionAleatoria(direcciones)
            if not self.portalDesactivado:
                if self.nodo.definirConexion[PORTAL] is not None:
                    self.nodo = self.nodo.definirConexion[PORTAL]
            self.objetivo = self.objetivoNuevo(direccion)
            if self.objetivo is not self.nodo:
                self.direcion = direccion
            else:
                self.objetivo = self.objetivoNuevo(self.direccion)

            self.setPosicion()                
            
    def direccionesValidas(self):
        direcciones = []
        for key in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]:
            if self.direccionValida(key):
                if key != self.direcion * -1:
                    direcciones.append(key)
        if len(direcciones) == 0:
            direcciones.append(self.direcion * -1)
            return direcciones
        
    def direccionAleatoria(self, direcciones):
        return direcciones[randint(0, len(direcciones)-1)]
             