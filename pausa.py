class Pausa(object):
    def __init__(self, pausa = False):
        self.pausa = pausa
        self.timer = 0
        self.tiempoPausa = None
        self.func = None

    def actualizar(self, dt):
        if self.tiempoPausa is not None:
            self.timer += dt
            if self.timer >= self.tiempoPausa:
                self.timer = 0
                self.pausa = False
                self.tiempoPausa = None
                return self.func
        return None
    
    def setPausa(self, jugadorPauso = False, tiempoPausa = None, func = None):
        self.timer = 0
        self.func = func
        self.timepo = tiempoPausa
        self.cambiar()

    def cambiar(self):
        self.pausa = not self.pausa