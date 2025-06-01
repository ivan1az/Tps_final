class Persona:
    def __init__(self, nombre, apellidoPaterno, apellidoMaterno, edad):
        if not nombre.strip():               
           raise AltaPersonaNombreException("Error: no debe estar vacio el campo nombre")
        
        if not apellidoPaterno.strip():  
            raise AltaPersonaNombreException("Error: no debe estar vacio el campo apellido_paterno")
        
        if edad <= 0:
            raise AltaPersonaEdadException("Error: la edad no debe ser menor igual a 0")

        self.nombre = nombre
        self.edad = edad
        self.apellidoPaterno = apellidoPaterno
        self.apellidoMaterno = apellidoMaterno

    
class AltaPersonaNombreException(Exception):
    pass


class AltaPersonaEdadException(Exception):
    pass