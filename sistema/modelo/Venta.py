from sistema.modelo.Producto import Producto, PrecioVentaErrorExcepcion,ExistenciaErrorException
from sistema.modelo.Usuarios import Usuarios
from sistema.modelo.Producto import Producto, AltaProductoError,PrecioVentaErrorExcepcion, ExistenciaErrorException
from sistema.extencion.extencion import pgdb 

class Venta(Producto):    
    def __init__(self, nombre_producto, tipo,precio_venta,existencia, fecha_venta,cantidad_vendida, descuento):
        super().__init__(nombre_producto,tipo ,precio_venta, existencia)

        if not nombre_producto.strip(): 
            raise AltaVentaError("La fecha de venta no puede estar vacía.")
        
        if descuento < 0: 
            raise AltaVentaError("Error: el descuento no puede ser menor a cero")
        

        if not fecha_venta.strip(): 
            raise AltaVentaError("La fecha de venta no puede estar vacía.")
        
        if cantidad_vendida <= 0:
            raise AltaVentaError("La cantidad vendida debe ser mayor a 0.")



        self.cantidad_vendida = int(cantidad_vendida)
        self.fecha_venta = fecha_venta
        self.cantidad_vendida = cantidad_vendida
        self.descuento = descuento

        
   
    @property
    def db(self):
        """Accede a la conexion global de la base de datos"""
        global pgdb
        if pgdb is None:
            raise DBException("La conexion a la base de datos no ha sido inicializada")
        return pgdb
    

       # Consultar los productos de la base de datos
    def consulta_ventas():
        resultados  = []
         # Obtener una conexión
        with pgdb.get_cursor() as cursor:
            # Ejecutar una consulta
            cursor.execute("SELECT * FROM ventas")
            # Obtener los resultados
            filas = cursor.fetchall()
            # Mostrar los resultados
            for fila in filas:
                print(fila)
                resultados.append(fila) 
           
        
        return resultados
    
    
    def agregar_venta(self, idvendedor):
        with self.db.get_cursor() as cursor:
                cursor.execute("SET client_encoding TO 'UTF8';")                         
                cursor.execute("""INSERT INTO ventas(nombre_producto, precio_venta, tipo, fecha_venta, cantidad_vendida, idvendedor, descuento)
                VALUES (%s, %s, %s, %s, %s, %s, %s);""", (
                self.nombre_producto,
                self.precio_venta,
                self.tipo,
                self.fecha_venta,
                self.cantidad_vendida,
                idvendedor,
                self.descuento
                ))
             
        

class DBException(Exception):
    pass


class CantidadVentaError(Exception):
    pass

class AltaVentaError(Exception):
    pass

class FechaVentaError(Exception):
    pass



