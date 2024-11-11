# Clase para pausar el juego, es bastante importante para animaciones a la hora de que PAcman come los fantasmas o muere, tambien al pasar el nivel y generar ciertas animaciones en el mismo.
class Pausador(object):
    def __init__(self, pausado = False):
        self.pausado = pausado
        self.timer = 0
        self.tiempoPausa = None
        self.func = None

    def actualizar(self, dt):
        if self.tiempoPausa is not None:
            self.timer += dt
            if self.timer >= self.tiempoPausa:
                self.timer = 0
                self.pausado = False
                self.tiempoPausa = None
                return self.func
        return None
    
    def setPausa(self, jugadorPauso = False, tiempoPausa = None, func = None):
        self.timer = 0
        self.func = func
        self.tiempoPausa = tiempoPausa
        self.cambiar()

    def cambiar(self):
        self.pausado = not self.pausado