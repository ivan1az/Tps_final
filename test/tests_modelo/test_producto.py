import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sistema.extencion.extencion import pgdb
from sistema.vista.inicio import create_app
from sistema.modelo.Producto import Producto,  PrecioVentaErrorExcepcion, ExistenciaErrorException, AltaProductoError
app = create_app()
app.config.update({
        "TESTING": True,
    })

   # Inicialización de la base de datos
print("...inicializando entorno de TESTING...")
pgdb.init_app(app)
pgdb.create_all_tables_productos()

def test_crear_instancia_producto():
    nombre_producto = 'playera seleccion mexicana'
    tipo = 'chica'
    precio_venta = 1200
    existencia = 5
    p = Producto(nombre_producto, tipo, precio_venta, existencia)
    assert  p.nombre_producto == nombre_producto
    assert  p.tipo == tipo
    assert  p.precio_venta == precio_venta
    assert  p.existencia == existencia

def test_crear_instancia_producto_precio_error():
    nombre_producto = 'playera seleccion mexicana'
    tipo = 'chica'
    precio_venta = -2000
    existencia = 5
    with pytest.raises(PrecioVentaErrorExcepcion) as e:
       p = Producto(nombre_producto, tipo, precio_venta, existencia)


def test_crear_instancia_producto_precio_error_2():
    nombre_producto = 'playera seleccion mexicana'
    tipo = 'chica'
    precio_venta = 1000000
    existencia = 5
    with pytest.raises(PrecioVentaErrorExcepcion) as e:
       p = Producto(nombre_producto, tipo, precio_venta, existencia)

def test_crear_producto_existencia_error():
    nombre_producto = 'playera seleccion mexicana'
    tipo = 'chica'
    precio_venta = 1000
    existencia = -1
    with pytest.raises(ExistenciaErrorException) as e:
       p = Producto(nombre_producto, tipo, precio_venta, existencia)

def tests_crear_producto_precio_error_3():
    nombre_producto = 'playera seleccion mexicana'
    tipo = 'chica'
    precio_venta =  "1000000" 
    existencia = 5
    with pytest.raises(PrecioVentaErrorExcepcion) as e:
       p = Producto(nombre_producto, tipo, precio_venta, existencia)

def tests_crear_producto_precio_error_4():
    nombre_producto = 'playera seleccion mexicana'
    tipo = 'chica'
    precio_venta =  "1000000as" 
    existencia = 5
    with pytest.raises(PrecioVentaErrorExcepcion) as e:
       p = Producto(nombre_producto, tipo, precio_venta, existencia)

def test_crear_producto_consultar_productos():
    nombre_producto = 'playera seleccion de Costa rica'
    tipo = 'grande'
    precio_venta = 1000
    existencia = 5
    p = Producto(nombre_producto, tipo, precio_venta, existencia)
    p.agregar_productos()
    resultados = Producto.consulta_productos()
    assert resultados[0][1] == nombre_producto
    assert resultados[0][2] == tipo
    assert resultados[0][3] == precio_venta
    assert resultados[0][4] == existencia


def test_insertar_productos():
    nombre_producto = 'playera seleccion de Costa rica'
    tipo = 'grande'
    precio_venta = 1000
    existencia = 5
    p = Producto(nombre_producto, tipo, precio_venta, existencia)
    p.agregar_productos()
    producto = p.buscar_producto_nombre(nombre_producto)
    assert producto[0][1] == p.nombre_producto
    assert producto[0][2] == p.tipo
    assert float(producto[0][3]) == p.precio_venta
    assert float(producto[0][4]) == p.existencia

def test_busqueda_producto_id():
    id_producto = 1
    result = Producto.buscar_producto(id_producto)
    assert result[0][0] == id_producto

def test_busqueda_producto_nombre_error():
    nombre_producto = "Camisa playera seleccion de los Estados Unidos"
    with pytest.raises(AltaProductoError):
        res = Producto.buscar_producto_nombre(nombre_producto)
        
def test_busqueda_producto_id_error():
    id_producto = 100  
    with pytest.raises(AltaProductoError):
        res = Producto.buscar_producto(id_producto)

def test_eliminar_producto():
    nombre_producto = 'playera seleccion de Costa rica'
    tipo = 'grande'
    precio_venta = 1000
    existencia = 5
    p = Producto(nombre_producto, tipo, precio_venta, existencia)
    p.agregar_productos()
    producto_encontrado = p.buscar_producto_nombre(nombre_producto)
    id_producto = producto_encontrado[0][0]  
    Producto.eliminar_producto(id_producto)
   
    with pytest.raises(AltaProductoError):
        Producto.buscar_producto(id_producto)

def test_modificar_producto():
    id_producto = 2
    nombre_producto = 'playera seleccion de Costa rica'
    tipo = 'grande'
    precio_venta = 1000
    existencia = 5
    producto = Producto(nombre_producto,tipo,precio_venta,existencia)
    producto.modificar_producto(id_producto)
    res = Producto.buscar_producto(id_producto)
    assert res[0][0] == id_producto
    assert res[0][1] == nombre_producto
    assert res[0][2] == tipo
    assert res[0][3] == precio_venta
    assert res[0][4] == existencia

def test_descontar_producto():
    nombre_producto = 'playera seleccion de Costa rica'
    tipo = 'grande'
    precio_venta = 1000
    existencia = 5
    p = Producto(nombre_producto, tipo, precio_venta, existencia)
    p.agregar_productos()
    p.descontar_existencia(4, 1)
    resultados = Producto.consulta_productos()
    assert resultados[0][1] == nombre_producto
    assert resultados[0][2] == tipo
    assert resultados[0][3] == precio_venta
    assert resultados[0][4] == existencia