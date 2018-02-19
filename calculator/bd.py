"""
Clase base de datos con dos metodos, uno que ayuda a guardar sesion a la bd
y otro que ayuda a restaurar los datos buscandolos por el nombre guardado
"""
class database(object):

    def __init__(self):
        self.dict = {}

    def add_bd(self,name, calculo):
        if name in self.dict.keys():
            return False
        else:
            self.dict[name] = calculo
            return True

    def from_bd(self, name):
        if name in self.dict.keys():
            return self.dict[name]
        else:
            return ""
