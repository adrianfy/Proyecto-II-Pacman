import math

class Vector (object):
    def __init__(self,x=0, y=0):
        self.x = x
        self.y = y
        self.thresh = 0.00001

    def __sumar__(self, other):
        return Vector(self.x + other.x,self.y + other.y)
    
    def __restar__(self, other):
        return Vector(self.x - other.x,self.y - other.y)
    
    def __negacion__(self):
        return Vector(-self.x,-self.y)

    def __multiplicacion__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __division__(self,scalar):
        if scalar !=0:
            return Vector(self.x / float(scalar), self.y / float(scalar))
        return None
    
    def __divisionReal__(self,scalar):
        return self.__div__(scalar)
    
    def __igualdad__(self,other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    def magnitudCuadrados(self):
        return self.x**2 + self.y**2
    
    def magnitud(self):
        return math.sqrt(self.magnitudCuadrados())
    
    def copia(self):
        return Vector(self.x, self.y)
    
    def coordebadaTupla(self):  #Las tuplas son estructuras que permiten agrupar valores y son útiles para representar un par de coordenadas
        return self.x,self.y

    def coordenadaEntero(self):
        return int (self.x), int(self.y)
    
    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"
    
    

                            


























