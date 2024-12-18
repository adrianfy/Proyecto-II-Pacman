import pygame
from pygame.locals import *
from vector import Vector
from constantes import *
from random import randint

class Entidad(object):
    def __init__(self, nodo): #Inicializa la entidad con una direccion y una posicion inicial
        self.nombre = None
        self.direcciones = {ARRIBA:Vector(0, -1),ABAJO:Vector(0,1), IZQUIERDA:Vector(-1, 0), DERECHA:Vector(1, 0), DETENER:Vector()}
        self.direccion = DETENER
        self.setVelocidad(100)
        self.radio = 10
        self.radioColision = 5
        self.color = BLANCO
        self.visibilidad = True
        self.portalDesactivado = False
        self.meta = None
        self.metodoDireccion = self.direccionMeta
        self.setNodoInicial(nodo)
        self.imagen = None

    def actualizar(self, dt):#Actualiza la posicion de la entidad
        self.posicion += self.direcciones[self.direccion]*self.velocidad*dt

        if self.objetivoRebasado():
            self.nodo = self.objetivo
            direcciones = self.direccionesValidas()
            direccion = self.metodoDireccion(direcciones)
            if not self.portalDesactivado:
                if self.nodo.definirConexion[PORTAL] is not None:
                    self.nodo = self.nodo.definirConexion[PORTAL]
            self.objetivo = self.objetivoNuevo(direccion)
            if self.objetivo is not self.nodo:
                self.direccion = direccion
            else:
                self.objetivo = self.objetivoNuevo(self.direccion)

            self.setPosicion()                
               
    def direccionValida(self, direccion):#Verifica si la direccion es valida
        if direccion is not DETENER:
            if self.nombre in self.nodo.acceso[direccion]:
              if self.nodo.definirConexion[direccion] is not None:
                 return True
        return False

    def objetivoNuevo(self, direccion):#Define el nuevo objetivo
        if self.direccionValida(direccion):
            return self.nodo.definirConexion[direccion]
        return self.nodo

    def objetivoRebasado(self):#Verifica si el objetivo ha sido rebasado
        if self.objetivo is not None:
            vec1 = self.objetivo.posicion - self.nodo.posicion
            vec2 = self.posicion - self.nodo.posicion
            nodoObjetivo = vec1.magnitudCuadrados()
            nodoSelf = vec2.magnitudCuadrados()
            return nodoSelf >= nodoObjetivo
        return False

    def direccionInversa(self):#Cambia la direccion de la entidad
        self.direccion *= -1
        temp = self.nodo
        self.nodo = self.objetivo
        self.objetivo = temp

    def direccionOpuesta(self, direccion):#Verifica si la direccion es opuesta
        if direccion is not DETENER:
            if direccion == self.direccion * -1:
                return True
        return False

    def setVelocidad(self, velocidad):#Define la velocidad de la entidad
        self.velocidad = velocidad * ANCHOCASILLA / 16

    def direccionesValidas(self):#Verifica las direcciones validas
        direcciones = []
        for key in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]:
            if self.direccionValida(key):
                if key != self.direccion * -1:
                    direcciones.append(key)
        if len(direcciones) == 0:
            direcciones.append(self.direccion * -1)
        return direcciones
        
    def direccionAleatoria(self, direcciones):#Define una direccion aleatoria
        return direcciones[randint(0, len(direcciones)-1)]

    def direccionMeta(self, direcciones):#Define la direccion de la entidad
        distancias = []
        for direccion in direcciones:
            vec = self.nodo.posicion + self.direcciones[direccion]*ANCHOCASILLA - self.meta
            distancias.append(vec.magnitudCuadrados())
        indice = distancias.index(min(distancias))
        return direcciones[indice]
    
    def setNodoInicial(self, nodo):#Define el nodo inicial de la entidad
        self.nodo = nodo
        self.nodoInicial = nodo
        self.objetivo = nodo
        self.setPosicion()
    
    def setEntreNodos(self, direccion):
        if self.nodo.definirConexion[direccion] is not None:
            self.objetivo = self.nodo.definirConexion[direccion]
            self.posicion = (self.nodo.posicion + self.objetivo.posicion) / 2.0

    def setPosicion(self):
        self.posicion = self.nodo.posicion.copia()

    def reiniciar(self):
        self.setNodoInicial(self.nodoInicial)
        self.direccion = DETENER
        self.velocidad = 100
        self.visibilidad = True

    def renderizar(self, pantalla):#Dibuja la entidad en la pantalla
        if self.visibilidad:
            if self.imagen is not None:
                ajustar = Vector(ANCHOCASILLA, ALTOCASILLA) / 2
                p = self.posicion - ajustar
                pantalla.blit(self.imagen, p.coordenadaTupla())
            else:
                p = self.posicion.coordenadaInt()
                pygame.draw.circle(pantalla, self.color, p, self.radio)