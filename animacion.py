from constantes import*
# La clase animacion se encarga de mostrar una secuencia de imagenes a una velocidad determinada

class Animador(object):
    # Inicializa la animacion con una lista de cuadros, una velocidad y un bucle especifico
    def __init__(self, cuadros=[], velocidad=20, bucle=True):
        self.cuadros = cuadros
        self.actual_cuadros = 0
        self.velocidad = velocidad
        self.bucle = bucle
        self.dt = 0
        self.finalizado = False
    
    # Reinicia la animacion
    def reiniciar(self):
        self.actual_cuadros = 0
        self.finalizado = False

    # Actualiza la animacion
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
    
    # Cambia al siguiente cuadro (imagen) para dar la sensacion de movimiento
    def siguienteCuadro(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.velocidad):
            self.actual_cuadros += 1
            self.dt = 0