from constantes import *

#En esta clase se encuentra los comportamiendos de los fantasmas


class ModoPrincipal(object):
    def __init__(self): #Inicializa el modo de los fantasmas
        self.timer = 0
        self.dispersion()

    def actualizar(self, dt): #Actualiza el modo actual en funcion al tiempo transcurrido
        self.timer += dt
        if self.timer >= self.tiempo:
            if self.modo is DISPERCION:
                self.perseguir()
            elif self.modo is PERSEGUIR:
                self.dispersion()

    def dispersion(self):# Se cambia el modo de los fantasmas a dispersion
        self.modo = DISPERCION
        self.tiempo = 7
        self.time = 0

    def perseguir(self):#Se cambia el modo de los fantasmas a perseguir
        self.modo = PERSEGUIR
        self.tiempo = 20
        self.timer = 0

class ModoControlador(object):#El controlador gestiona el modo de cada fantasma individualmente
    def __init__(self, entidad):#Inicia el controlador del modo fantasma
        self.timer = 0
        self.tiempo = None
        self.modoPrincipal = ModoPrincipal()
        self.actual = self.modoPrincipal.modo
        self.entidad = entidad

    def actualizar(self, dt):#Actualiza el estado del fantamas
        self.modoPrincipal.actualizar(dt)
        if self.actual is ASUSTADO:
            self.timer += dt
            if self.timer >= self.tiempo:
                self.tiempo = None
                self.entidad.modoNormal()
                self.actual = self.modoPrincipal.modo
        elif self.actual in [DISPERCION, PERSEGUIR]:
             self.actual = self.modoPrincipal.modo
            
        if self.actual is SPAWN:
            if self.entidad.nodo == self.entidad.spawnNodo:
                self.entidad.modoNormal()
                self.actual = self.modoPrincipal.modo

    def setSpawnModo(self):#Modo spawn, los fantamas regresan a su posición original
        if self.actual is ASUSTADO:
            self.actual = SPAWN                

    def setModoAsustado(self):#Modo asustado, los fantasmas se vuelven vulnerables y llegar a se comidos
        if self.actual in [DISPERCION,PERSEGUIR]:
            self.timer = 0
            self.tiempo = 7
            self.actual = ASUSTADO
        elif self.actual is ASUSTADO:
            self.timer = 0