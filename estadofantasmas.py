from constantes import *

class ModoPrincipal(object):
    def __init__(self):
        self.timer = 0
        self.dispersion()

    def actualizar(self, dt):
        self.timer += dt
        if self.timer >= self.tiempo:
            if self.modo is DISPERCION:
                self.perseguir()
            elif self.modo is PERSEGUIR:
                self.dispersion()

    def dispersion(self):
        self.modo = DISPERCION
        self.tiempo = 7
        self.time = 0

    def perseguir(self):
        self.modo = PERSEGUIR
        self.tiempo = 20
        self.timer = 0

class ModoControlador(object):
    def __init__(self, entidad):
        self.timer = 0
        self.tiempo = None
        self.modoPrincipal = ModoPrincipal()
        self.actual = self.modoPrincipal.modo
        self.entidad = entidad

    def actualizar(self, dt):
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

    def setSpawnModo(self):
        if self.actual is ASUSTADO:
            self.actual = SPAWN                

    def setModoAsustado(self):
        if self.actual in [DISPERCION,PERSEGUIR]:
            self.timer = 0
            self.tiempo = 7
            self.actual = ASUSTADO
        elif self.actual is ASUSTADO:
            self.timer = 0




