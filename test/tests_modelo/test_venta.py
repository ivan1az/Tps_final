import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sistema.extencion.extencion import pgdb
from sistema.vista.inicio import create_app
from sistema.modelo.Venta import Venta, AltaVentaError,ExistenciaErrorException
from sistema.modelo.Producto import Producto, PrecioVentaErrorExcepcion, ExistenciaErrorException
app = create_app()
app.config.update({
        "TESTING": True,
    })

   # Inicialización de la base de datos
print("...inicializando entorno de TESTING...")
pgdb.init_app(app)
pgdb.create_all_tables_ventas()


def test_crear_venta():
    nombre_producto = 'Playera seleccion mexicana'
    tipo = "Chica"
    precio_venta = 1200
    existencia = 5
    fecha_venta = "10/05/25"
    cantidad_vendida = 1
    descuento = 0.1
   
    v = Venta(nombre_producto,tipo,precio_venta,existencia, fecha_venta, cantidad_vendida, descuento)
    assert  v.nombre_producto == nombre_producto
    assert  v.tipo == tipo
    assert  v.precio_venta == precio_venta
    assert  v.existencia == existencia
    assert  v.fecha_venta == fecha_venta
    assert  v.cantidad_vendida == cantidad_vendida   
    assert  v.descuento == descuento
    

def test_crear_venta_cantidad_error():
    nombre_producto = 'Playera seleccion mexicana'
    tipo = "Chica"
    precio_venta = 1200
    existencia = 5
    fecha_venta = "10/05/25"
    cantidad_vendida = 0
    descuento = 0.1
    with pytest.raises(AltaVentaError) as e:
        v = Venta(nombre_producto,tipo,precio_venta,existencia, fecha_venta, cantidad_vendida, descuento )


def test_crear_instancia_venta_nombre_error():
    nombre_producto = ''
    tipo = "Chica"
    precio_venta = 1200
    existencia = 5
    fecha_venta = "10/05/25"
    cantidad_vendida = 1
    descuento = 0.1
    with pytest.raises(AltaVentaError) as e:
        v = Venta(nombre_producto,tipo,precio_venta,existencia, fecha_venta, cantidad_vendida, descuento )


def test_crear_instancia_venta_precio_venta_error():
    nombre_producto = 'Playera seleccion mexicana'
    tipo = "Chica"
    precio_venta = -1
    existencia = 5
    fecha_venta = "10/05/25"
    cantidad_vendida = 1
    descuento = 0.1
    with pytest.raises(PrecioVentaErrorExcepcion) as e:
        v = Venta(nombre_producto,tipo,precio_venta,existencia, fecha_venta, cantidad_vendida, descuento )


def test_crear_instancia_venta_existencia_error():
    nombre_producto = 'Playera seleccion mexicana'
    tipo = "Chica"
    precio_venta = 1200
    existencia = -1
    fecha_venta = "10/05/25"
    cantidad_vendida = 1
    descuento = 0.1
    with pytest.raises(ExistenciaErrorException) as e:
        v = Venta(nombre_producto,tipo,precio_venta,existencia, fecha_venta, cantidad_vendida, descuento )


def test_crear_venta_descuento_error():
    nombre_producto = 'Playera seleccion mexicana'
    tipo = "Chica"
    precio_venta = 1200
    existencia = 5
    fecha_venta = "10/05/25"
    cantidad_vendida = 1
    descuento = -1
    with pytest.raises(AltaVentaError) as e:
        v = Venta(nombre_producto,tipo,precio_venta,existencia, fecha_venta, cantidad_vendida, descuento )


def test_crear_instancia_venta_fecha_error():
    nombre_producto = 'Playera seleccion mexicana'
    tipo = "Chica"
    precio_venta = 1200
    existencia = 5
    fecha_venta = ""
    cantidad_vendida = 1
    descuento = 0.1
    with pytest.raises(AltaVentaError) as e:
        v = Venta(nombre_producto,tipo,precio_venta,existencia, fecha_venta, cantidad_vendida, descuento )

def test_crear_venta_cosultar_ventas():
    nombre_producto = 'Playera seleccion mexicana'
    tipo = "Chica"
    precio_venta = 1200
    existencia = 5
    fecha_venta = "10/05/25"
    cantidad_vendida = 1
    id_vendedor = 3
    descuento = 0.1
    v = Venta(nombre_producto,tipo,precio_venta,existencia, fecha_venta, cantidad_vendida, descuento)
    v.agregar_venta(id_vendedor)
    resultados = Venta.consulta_ventas()
    assert resultados[0][1] == nombre_producto
    assert float(resultados[0][2]) == precio_venta
    assert resultados[0][3] == tipo
    assert resultados[0][4] == fecha_venta
    assert int(resultados[0][5]) == cantidad_vendida
    assert resultados[0][6] == id_vendedor
    assert float(resultados[0][7]) == descuento



    



   





