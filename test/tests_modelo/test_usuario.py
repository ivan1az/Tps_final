import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sistema.extencion.extencion import pgdb
from sistema.vista.inicio import create_app
from sistema.modelo.Usuarios import Usuarios, AltaUsuariosException, AltaUsuariosSueldoException
from sistema.modelo.Persona import Persona, AltaPersonaEdadException, AltaPersonaNombreException
app = create_app()
app.config.update({
        "TESTING": True,
    })

   # Inicialización de la base de datos
print("...inicializando entorno de TESTING...")
pgdb.init_app(app)
pgdb.create_all_tables_usuarios()


def test_crear_instancia_usuario():
    nombre = 'Juan'
    apellidoPaterno = 'Pérez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.10
    contrasenia = "12345"
    numero_telefono = "5524904550"
    sueldo = 10000
    us = Usuarios(nombre,  apellidoPaterno,apellidoMaterno,edad, perfil, comision, contrasenia, numero_telefono, sueldo )
    assert  us.nombre == nombre
    assert  us.apellidoPaterno == apellidoPaterno
    assert  us.apellidoMaterno == apellidoMaterno
    assert  us.edad == edad
    assert  us.perfil == perfil
    assert  us.comision == comision
    assert  us.contrasenia == contrasenia
    assert  us.numero_telefono == numero_telefono
    assert  us.sueldo == sueldo


def test_crear_instancia_usuario_sueldo_error():
    nombre = 'Juan'
    apellidoPaterno = 'Pérez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.10
    contrasenia = "12345"
    numero_telefono = "5524904550"
    sueldo = -1
    with pytest.raises( AltaUsuariosSueldoException) as e:
        us = Usuarios(nombre,  apellidoPaterno,apellidoMaterno,edad, perfil, comision, contrasenia, numero_telefono, sueldo )


def test_crear_instancia_usuario_sueldo_error_2():
    nombre = 'Juan'
    apellidoPaterno = 'Pérez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.10
    contrasenia = "12345"
    numero_telefono = "5524904550"
    sueldo = 100000
    with pytest.raises( AltaUsuariosSueldoException) as e:
        us = Usuarios(nombre,  apellidoPaterno,apellidoMaterno,edad, perfil, comision, contrasenia, numero_telefono, sueldo )


def test_crear_instancia_usuario_edad_error():
    nombre = 'Juan'
    apellidoPaterno = 'Pérez'
    apellidoMaterno = 'Rodriguez'
    edad = -15
    perfil = "Vendedor"
    comision = 0.10
    contrasenia = "12345"
    numero_telefono = "5524904550"
    sueldo = 100000
    with pytest.raises(AltaPersonaEdadException) as e:
       us = Usuarios(nombre,  apellidoPaterno,apellidoMaterno,edad, perfil, comision, contrasenia, numero_telefono, sueldo )

def test_crear_instancia_usuario_sueldo_error():
    nombre = 'Juan'
    apellidoPaterno = 'Perez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.10
    contrasenia = "12345"
    numero_telefono = "5524904550"
    sueldo = -1
    with pytest.raises( AltaUsuariosSueldoException) as e:
       us = Usuarios(nombre,  apellidoPaterno,apellidoMaterno,edad, perfil, comision, contrasenia, numero_telefono, sueldo )

def test_crear_instancia_usuario_comision_error():
    nombre = 'Juan'
    apellidoPaterno = 'Perez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = -1
    contrasenia = "12345"
    numero_telefono = "5524904550"
    sueldo = 10000
    with pytest.raises(AltaUsuariosException) as e:
       us = Usuarios(nombre,  apellidoPaterno,apellidoMaterno,edad, perfil, comision, contrasenia, numero_telefono, sueldo )


def test_crear_instancia_usuario_contrasenia_error():
    nombre = 'Juan'
    apellidoPaterno = 'Perez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.1
    contrasenia = ""
    numero_telefono = "5524904550"
    sueldo = 10000
    with pytest.raises(AltaUsuariosException) as e:
       us = Usuarios(nombre,  apellidoPaterno,apellidoMaterno,edad, perfil, comision, contrasenia, numero_telefono, sueldo )

def tests_crear_instancia_usuario_sueldo_error_3():
    nombre = 'Juan'
    apellidoPaterno = 'Perez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.1
    contrasenia = ""
    numero_telefono = "5524904550"
    sueldo = "100000000"
    with pytest.raises(AltaUsuariosSueldoException) as e:
        us = Usuarios(nombre,  apellidoPaterno,apellidoMaterno,edad, perfil, comision, contrasenia, numero_telefono, sueldo )


def tests_crear_instancia_usuario_sueldo_error_4():
    nombre = 'Juan'
    apellidoPaterno = 'Perez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.1
    contrasenia = "8314"
    numero_telefono = "5524904550"
    sueldo = "100000000sa"
    with pytest.raises(AltaUsuariosSueldoException) as e:
        us = Usuarios(nombre,  apellidoPaterno,apellidoMaterno,edad, perfil, comision, contrasenia, numero_telefono, sueldo )

def tests_crear_instancia_usuario_sueldo_error_5():
    nombre = 'Juan'
    apellidoPaterno = 'Perez'
    apellidoMaterno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.1
    contrasenia = "8314"
    numero_telefono = "5524904550"
    sueldo = 0
    with pytest.raises(AltaUsuariosSueldoException) as e:
        us = Usuarios(nombre,  apellidoPaterno,apellidoMaterno,edad, perfil, comision, contrasenia, numero_telefono, sueldo )

def test_consulta_usuarios():
    nombre = 'Juan'
    apellido_paterno = 'Perez'
    apellido_materno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.10
    contrasenia = "8314"
    numero_telefono = "5524904550"
    sueldo = 10000
    usuario = Usuarios(nombre, apellido_paterno, apellido_materno, edad, perfil, comision,contrasenia,numero_telefono,sueldo)
    usuario.agregar_usuarios()
    resultados = Usuarios.consulta_usuarios()
    assert resultados[0][0] == 1
    assert resultados[0][1] == usuario.nombre
    assert resultados[0][2] == usuario.apellidoPaterno
    assert resultados[0][3] == usuario.apellidoMaterno
    assert resultados[0][4] == usuario.edad
    assert resultados[0][5] == usuario.perfil
    assert float(resultados[0][6]) == usuario.comision
    assert resultados[0][7] == usuario.contrasenia
    assert resultados[0][8] == usuario.numero_telefono
    assert resultados[0][9] == usuario.sueldo
    
def test_insertar_usuarios():
    nombre = 'Juan'
    apellido_paterno = 'Perez'
    apellido_materno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.1
    contrasenia = "8314"
    numero_telefono = "5524904550"
    sueldo = 10000
    usuario = Usuarios(nombre, apellido_paterno, apellido_materno, edad, perfil, comision,contrasenia,numero_telefono,sueldo)
    usuario.agregar_usuarios()
    us = usuario.buscar_usuario(1)
    assert us[0][1] == usuario.nombre
    assert us[0][2] == usuario.apellidoPaterno
    assert us[0][3] == usuario.apellidoMaterno
    assert int(us[0][4]) == usuario.edad
    assert us[0][5] == usuario.perfil
    assert float(us[0][6]) == usuario.comision
    assert us[0][7] == usuario.contrasenia
    assert us[0][8] == usuario.numero_telefono
    assert int(us[0][9]) == usuario.sueldo

def test_buscar_usuario_inexistente():
    id_vendedor = 3
    with pytest.raises(AltaUsuariosException):
        res = Usuarios.buscar_usuario(id_vendedor)

def test_eliminar_usuario():
    id_vendedor =2
    nombre = 'Juan'
    apellido_paterno = 'Perez'
    apellido_materno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.1
    contrasenia = "8314"
    numero_telefono = "5524904550"
    sueldo = 10000
    usuario = Usuarios(nombre, apellido_paterno, apellido_materno, edad, perfil, comision,contrasenia,numero_telefono,sueldo)
    usuario.agregar_usuarios()
    usuario_encontrado = usuario.buscar_usuario(id_vendedor)
    Usuarios.eliminar_usuario(id_vendedor)
    with pytest.raises( AltaUsuariosException):
        nueva_busqueda = usuario.buscar_usuario(id_vendedor)

def test_modificar_usuario():
    id_vendedor =1
    nombre = 'Juan'
    apellido_paterno = 'Perez'
    apellido_materno = 'Rodriguez'
    edad = 30
    perfil = "Administrador"
    comision = 0
    contrasenia = "8314"
    numero_telefono = "5524904550"
    sueldo = 10000
    usuario = Usuarios(nombre, apellido_paterno, apellido_materno, edad, perfil, comision,contrasenia,numero_telefono,sueldo)
    usuario.modificar_vendedor(id_vendedor)
    res = Usuarios.buscar_usuario(id_vendedor)
    assert res[0][0] == id_vendedor
    assert res[0][1] == nombre
    assert res[0][2] == apellido_paterno
    assert res[0][3] == apellido_materno
    assert res[0][4] == edad
    assert res[0][5] == perfil
    assert res[0][6] == comision
    assert res[0][7] == contrasenia
    assert res[0][8] == numero_telefono
    assert res[0][9] == sueldo


def test_buscar_usuario_por_nombre():
    nombre = 'Osvaldo'
    apellido_paterno = 'Perez'
    apellido_materno = 'Rodriguez'
    edad = 30
    perfil = "Vendedor"
    comision = 0.1
    contrasenia = "5692"
    numero_telefono = "5524904550"
    sueldo = 10000
    usuario = Usuarios(nombre, apellido_paterno, apellido_materno, edad, perfil, comision,contrasenia,numero_telefono,sueldo)
    usuario.agregar_usuarios()
    res = Usuarios.buscar_usuario_por_nombre(nombre)
    assert res[0][1] == nombre
    assert res[0][2] == apellido_paterno
    assert res[0][3] == apellido_materno
    assert int(res[0][4]) == edad
    assert res[0][5] == perfil
    assert float(res[0][6]) == comision
    assert res[0][7] == contrasenia
    assert res[0][8] == numero_telefono
    assert int(res[0][9]) == sueldo

def test_buscar_usuario_por_nombre_error():
    nombre = "Carlos"
    with pytest.raises(AltaUsuariosException):
        res = Usuarios.buscar_usuario_por_nombre(nombre)