import math

# Durante la creacion de esta clase nos dimos cuenta que existen metodos propios de python definidos por guiones bajos (__nombre__)
# estos metodos son llamados metodos especiales y son utilizados para definir comportamientos especiales de los objetos, por ejemplo
# __add__, __sub__, __mul__, __div__, __truediv__, __neg__, __eq__, __str__, etc.

class Vector (object):
    def __init__(self,x = 0, y = 0):
        self.x = x
        self.y = y
        self.thresh = 0.000001

    # Suma de vectores
    def __add__(self, other):
        return Vector(self.x + other.x,self.y + other.y)
    
    # Resta de vectores
    def __sub__(self, other):
        return Vector(self.x - other.x,self.y - other.y)
    
    # Negacion de vectores
    def __neg__(self):
        return Vector(-self.x, -self.y)

    # Multiplicacion de vectores
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    # Divison de vectores
    def __div__(self,scalar):
        if scalar !=0:
            return Vector(self.x / float(scalar), self.y / float(scalar))
        return None
    
    # Divison Real de vectores
    def __truediv__(self,scalar):
        return self.__div__(scalar)
    
    # Igualdad de vectores
    def __eq__(self,other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    # Diferencia de vectores
    def magnitudCuadrados(self):
        return self.x**2 + self.y**2
    
    # Magnitud de vectores
    def magnitud(self):
        return math.sqrt(self.magnitudCuadrados())
    
    # Una copia del Vector
    def copia(self):
        return Vector(self.x, self.y)
    
    def coordenadaTupla(self):  #Las tuplas son estructuras que permiten agrupar valores y son útiles para representar un par de coordenadas
        return self.x, self.y

    def coordenadaInt(self):
        return int (self.x), int(self.y)
    
    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"
    
    # Metodo que recibe la propia clase y un diccionario, y retorna una nueva instancia de la clase con los valores del diccionario
    # el @ es un decorador que se utiliza para modificar funciones o metodos
    @classmethod
    def from_dict(cls, data):
        return cls(data["x"], data["y"])
    
    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y
        }
    
    

                            


























