import re

class User:
    def __init__(self, cedula, nombre_usuario, contrasena):
        self.contrasena = contrasena

        if not re.match(r'[a-z A-Z áéíóúñÑ]{2,255}', nombre_usuario):
            raise ValueError('El nombre debe tener más de dos palabras.')

        self.nombre_usuario = nombre_usuario

        if not cedula.isdigit() or len(cedula) < 4:
            raise ValueError('La cédula debe ser un número de minimo 4 dígitos.')

        self.cedula = cedula

    def toDict(self):
        return{
            "cedula" : self.cedula,
            "nombre_usuario" : self.nombre_usuario,
            "contrasena" : self.contrasena
        }
