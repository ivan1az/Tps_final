import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sistema.extencion.extencion import pgdb
from sistema.vista.inicio import create_app
from sistema.modelo.Persona import Persona, AltaPersonaNombreException, AltaPersonaEdadException
app = create_app()
app.config.update({
        "TESTING": True,
    })

   # Inicialización de la base de datos
print("...inicializando entorno de TESTING...")
pgdb.init_app(app)
#pgdb.create_all_tables()

def test_crear_persona():
    nombre = 'Juan'
    apellidoPaterno = 'Pérez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    p = Persona(nombre=nombre, apellidoPaterno=apellidoPaterno, apellidoMaterno=apellidoMaterno, edad=edad)
    assert  p.nombre == nombre
    assert  p.apellidoPaterno == apellidoPaterno
    assert  p.apellidoMaterno == apellidoMaterno
    assert  p.edad == edad

def test_crear_persona_edad_error():
    nombre = "Juan"
    apellidoPaterno = 'Pérez'
    apellidoMaterno = 'Rodriguez'
    edad = -1
    with pytest.raises(AltaPersonaEdadException) as e:
       p = Persona(nombre, apellidoPaterno, apellidoMaterno, edad)

def test_crear_persona_nombre_error():
    nombre = ''
    apellidoPaterno = 'Pérez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    with pytest.raises(AltaPersonaNombreException) as e:
       p = Persona(nombre, apellidoPaterno, apellidoMaterno, edad)

def test_crear_persona_nombre_error_2():
    nombre = "Juan"
    apellidoPaterno = ''
    apellidoMaterno = 'Rodriguez'
    edad = 30
    with pytest.raises(AltaPersonaNombreException) as e:
       p = Persona(nombre, apellidoPaterno, apellidoMaterno, edad)
