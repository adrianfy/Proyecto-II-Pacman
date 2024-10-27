from constantes import *

class ModoPrincipal(object):
    def __init__(self):
        self.dispersion()
        self.timer = 0

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
        self.entidad =entidad

    def actualizar(self, dt):
        self.modoPrincipal.actualizar(dt)
        if self.actual is CARGA:
            self.timer += dt
            if self.timer >= self.tiempo:
                self.tiempo = None
                self.entidad.modoNormal()
                self.actual = self.modoPrincipal.modo
            else:
              self.actual = self.modoPrincipal.modo 
        


    def setModoCarga(self):
        if self.actual in [DISPERCION,PERSEGUIR]:
            self.timer = 0
            self.time = 7
            self.actual = CARGA
        elif self.actual is CARGA:
            self.timer = 0




