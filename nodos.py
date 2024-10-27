import pygame
from vector import Vector
from constantes import *
import numpy as np

class Nodo(object):
    def __init__(self, x, y):
        self.posicion = Vector(x,y)
        self.definirConexion = {ARRIBA:None, ABAJO:None,IZQUIERDA:None, DERECHA:None, PORTAL:None}

    def renderizar(self, pantalla):
        for n in self.definirConexion.keys():
            if self.definirConexion[n] is not None:
                linea_inicio = self.posicion.coordenadaTupla()
                linea_final = self.definirConexion[n].posicion.coordenadaTupla()
                pygame.draw.line(pantalla, BLANCO, linea_inicio, linea_final, 4)
                pygame.draw.circle(pantalla, ROJO, self.posicion.coordenadaInt(), 12)

class GrupoNodos(object):
    def __init__(self, nivel):
        self.nivel = nivel
        self.nodosLUT = {}  # LUT significa "Look Up Table" (tabla de consulta)
        self.simbolosNodo = ['+','P', 'n']
        self.simbolosCamino = ['.','-', '|', 'p']
        data = self.leerLaberinto(nivel)
        self.crearTablaNodo(data)
        self.conectarHorizontal(data)
        self.conectarVertical(data)
        self.casita = None

    def leerLaberinto(self, textfile):
        return np.loadtxt(textfile,dtype='<U1')
    
    def crearTablaNodo(self, data, xoffset=0, yoffset=0):
        for fila in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                x,y = self.constructKey(col+xoffset, fila+yoffset)
                self.nodosLUT[(x, y)] = Nodo(x, y)
    
    def constructKey(self, x, y):
        return x * ANCHOCASILLA, y * ALTOCASILLA
    
    def conectarHorizontal(self, data, xoffset=0, yoffset=0):
        for fila in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[fila][col] in self.simbolosNodo:
                    if key is None:
                        key = self.constructKey(col+xoffset, fila+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, fila+yoffset)
                        self.nodosLUT[key].definirConexion[DERECHA] = self.nodosLUT[otherkey]
                        self.nodosLUT[otherkey].definirConexion[IZQUIERDA] = self.nodosLUT[key]
                        key = otherkey
                elif data[fila][col] not in self.simbolosCamino:
                    key = None

    def conectarVertical(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for fila in list(range(dataT.shape[1])):
                if dataT[col][fila] in self.simbolosNodo:
                    if key is None:
                        key = self.constructKey(col+xoffset, fila+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, fila+yoffset)
                        self.nodosLUT[key].definirConexion[ABAJO] = self.nodosLUT[otherkey]
                        self.nodosLUT[otherkey].definirConexion[ARRIBA] = self.nodosLUT[key]
                        key = otherkey
                elif dataT[col][fila] not in self.simbolosCamino:
                    key = None

    def getNododesdePixeles(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodosLUT.keys():
            return self.nodosLUT[(xpixel, ypixel)]
        return None

    def getNododesdeCasillas(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodosLUT.keys():
            return self.nodosLUT[(x, y)]
        return None
    
    def getIniciarNodoTemp(self):
        nodos = list(self.nodosLUT.values())
        return nodos[0]
    
    def setPortales(self, portal1, portal2):
        key1 = self.constructKey(*portal1)
        key2 = self.constructKey(*portal2)
        if key1 in self.nodosLUT.keys() and key2 in self.nodosLUT.keys():
            self.nodosLUT[key1].definirConexion[PORTAL] = self.nodosLUT[key2]
            self.nodosLUT[key2].definirConexion[PORTAL] = self.nodosLUT[key2]

    def crearCasitaFantasmas(self, xoffset, yoffset):
        casitadata = np.array([['X','X','+','X','X'],
                               ['X','X','.','X','X'],
                               ['+','X','.','X','+'],
                               ['+','.','+','.','+'],
                               ['+','X','X','X','+']])
        self.crearTablaNodo(casitadata, xoffset, yoffset)
        self.conectarHorizontal(casitadata, xoffset, yoffset)
        self.conectarVertical(casitadata,xoffset,yoffset)
        self.casita = self.constructKey(xoffset+2, yoffset)
        return self.casita
    
    def connectarNodosCasita(self, casita, otherkey, direccion):
        key = self.constructKey(*otherkey)
        self.nodosLUT[casita].definirConexion[direccion] = self.nodosLUT[key]
        self.nodosLUT[key].definirConexion[direccion*-1] = self.nodosLUT[casita]
    
    def renderizar(self, pantalla):
        for nodo in self.nodosLUT.values():
            nodo.renderizar(pantalla)