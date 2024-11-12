import pygame
from vector import Vector
from constantes import *
import numpy as np

# La clase Nodo se encarga de crear los nodos que se encuentran en el mapa
class Nodo(object):
    # Inicializa el nodo con una posicion y una definicion de conexion
    def __init__(self, x, y):
        self.posicion = Vector(x,y)
        self.definirConexion = {ARRIBA:None, ABAJO:None,IZQUIERDA:None, DERECHA:None, PORTAL:None}
        self.acceso ={ARRIBA:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA],
                      ABAJO:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA],
                      IZQUIERDA:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA],
                      DERECHA:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA]}

    # Convierte la posicion del nodo en una tupla
    def renderizar(self, pantalla):
        for n in self.definirConexion.keys():
            if self.definirConexion[n] is not None:
                linea_inicio = self.posicion.coordenadaTupla()
                linea_final = self.definirConexion[n].posicion.coordenadaTupla()
                pygame.draw.line(pantalla, BLANCO, linea_inicio, linea_final, 4)
                pygame.draw.circle(pantalla, ROJO, self.posicion.coordenadaInt(), 12)

    # Deniega el acceso a una entidad en una direccion especifica
    def accesoDenegado(self,direccion, entidad):
        if entidad.nombre in self.acceso[direccion]:
            self.acceso[direccion].remove(entidad.nombre)
    # Por el contrario, permite el acceso a una entidad en una direccion especifica
    def accesoPermitido(self, direccion, entidad):
        if entidad.nombre not in self.acceso[direccion]:
            self.acceso[direccion].append(entidad.nombre)

# La clase GrupoNodos se encarga de crear los nodos que se encuentran en el mapa
class GrupoNodos(object):
    # Inicializa el grupo de nodos con un nivel
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
    
    # Lee el laberinto desde un archivo de texto, esto hace que sea mas facil de modificar y agregar nuevos niveles (no agregamos diferentes mapas jeje)
    def leerLaberinto(self, textfile):
        return np.loadtxt(textfile,dtype='<U1')
    
    # Crea una tabla de nodos segun el laberinto
    def crearTablaNodo(self, data, xoffset=0, yoffset=0):
        for fila in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                x,y = self.constructKey(col+xoffset, fila+yoffset)
                self.nodosLUT[(x, y)] = Nodo(x, y)
    
    # Construye una clave para el diccionario de nodos
    # Esta retorna un valor unico que representa la posicion de un nodo
    # FUNCION HASH
    def constructKey(self, x, y):
        return x * ANCHOCASILLA, y * ALTOCASILLA
    
    # Conecta los nodos horizontalmente
    def conectarHorizontal(self, data, xoffset=0, yoffset=0):
        # Recorre el laberinto
        for fila in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                # Si encuentra un nodo, lo conecta con el nodo anterior
                if data[fila][col] in self.simbolosNodo:
                    # Si no hay un nodo anterior, se crea uno
                    if key is None:
                        key = self.constructKey(col+xoffset, fila+yoffset)
                    # Si hay un nodo anterior, se conecta con el nodo actual
                    else:
                        otherkey = self.constructKey(col+xoffset, fila+yoffset)
                        self.nodosLUT[key].definirConexion[DERECHA] = self.nodosLUT[otherkey]
                        self.nodosLUT[otherkey].definirConexion[IZQUIERDA] = self.nodosLUT[key]
                        key = otherkey
                    # Si no hay un nodo, se reinicia la clave
                elif data[fila][col] not in self.simbolosCamino:
                    key = None

    # Conecta los nodos verticalmente
    def conectarVertical(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        # Se hace lo mismo que el horizontal pero con las filas y columnas invertidas
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

    # Obtiene un nodo desde una posicion en pixeles
    def getNododesdePixeles(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodosLUT.keys():
            return self.nodosLUT[(xpixel, ypixel)]
        return None

    # Obtiene un nodo desde una posicion en casillas
    def getNododesdeCasillas(self, col, fila):
        x, y = self.constructKey(col, fila)
        if (x, y) in self.nodosLUT.keys():
            return self.nodosLUT[(x, y)]
        return None
    
    # Obtiene un nodo de inicio temporal
    def getIniciarNodoTemp(self):
        nodos = list(self.nodosLUT.values())
        return nodos[0]
    
    # Se encarga de crear una conexion entre dos nodos, estos seran los portales que transportan a Pacman y a los fantasmas de manera horizontal
    def setPortales(self, portal1, portal2):
        key1 = self.constructKey(*portal1)
        key2 = self.constructKey(*portal2)
        if key1 in self.nodosLUT.keys() and key2 in self.nodosLUT.keys():
            self.nodosLUT[key1].definirConexion[PORTAL] = self.nodosLUT[key2]
            self.nodosLUT[key2].definirConexion[PORTAL] = self.nodosLUT[key1]

    # Se encarga de crear una casita para los fantasmas, este es su spawn y su lugar seguro
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
    
    # Conecta los nodos de la casita con los nodos del mapa
    def connectarNodosCasita(self, casita, otherkey, direccion):
        key = self.constructKey(*otherkey)
        self.nodosLUT[casita].definirConexion[direccion] = self.nodosLUT[key]
        self.nodosLUT[key].definirConexion[direccion*-1] = self.nodosLUT[casita]
    
    # Renderiza los nodos
    def renderizar(self, pantalla):
        for nodo in self.nodosLUT.values():
            nodo.renderizar(pantalla)

    # Estos metodos se encargan de denegar o permitir el acceso a una entidad en una direccion especifica
    def accesoDenegado(self, col, fila, direccion, entidad):
        nodo = self.getNododesdeCasillas(col,fila)
        if nodo is not None:
            nodo.accesoDenegado(direccion,entidad)

    # Por el contrario, permite el acceso a una entidad en una direccion especifica
    def accesoPermitido(self, col, fila, direccion, entidad):
          nodo = self.getNododesdeCasillas(col,fila)
          if nodo is not None:
              nodo.accesoPermitido(direccion,entidad)

    def denegarAcessoLista(self, col, fila, direccion, entidades):
        for entidad in entidades:
            self.accesoDenegado(col, fila, direccion, entidad)

    def permitirAcessoLista(self, col, fila, direccion, entidades):
        for entidad in entidades:
            self.accesoPermitido(col, fila, direccion, entidad)

    def denegarAccesoCasita(self, entidad):
        self.nodosLUT[self.casita].accesoDenegado(ABAJO, entidad)

    def permitirAccesoCasita(self, entidad):
        self.nodosLUT[self.casita].accesoPermitido(ABAJO, entidad)

    # Aqui se niega el acceso a Pacman a la casita de los fantasmas o a los mismos durante la partida mientras no esten muertos.
    def denegarAccesoListaCasita(self, entidades):
        for entidad in entidades:
            self.denegarAccesoCasita(entidad)

    def permitirAccesoListaCasita(self, entidades):
        for entidad in entidades:
            self.permitirAccesoCasita(entidad)
        


    

