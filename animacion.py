from constantes import*

class Animador(object):
    def __init__(self, cuadros=[], velocidad=20, bucle=True):
        self.cuadros = cuadros
        self.actual_cuadros = 0
        self.velocidad = velocidad
        self.bucle = bucle
        self.dt = 0
        self.finalizado = False

    def reiniciar(self):
        self.actual_cuadros = 0
        self.finalizado = False

    def actualizar(self, dt):
        if not self.finalizado:
            self.siguienteCuadro(dt)
        if self.actual_cuadros == len(self.cuadros):
            if self.bucle:
                self.actual_cuadros = 0
            else:
                self.finalizado = True
                self.actual_cuadros -=1

        return self.cuadros[self.actual_cuadros]
    
    def siguienteCuadro(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.velocidad):
            self.actual_cuadros += 1
            self.dt = 0