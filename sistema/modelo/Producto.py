from sistema.extencion.extencion import pgdb 

class Producto:
    def __init__(self,nombre_producto,tipo, precio_venta, existencia):
        if isinstance(precio_venta, str):
            try:
                precio_venta = float(precio_venta)
            except:
                raise PrecioVentaErrorExcepcion("Error: el sueldo es inválido")
        
        if precio_venta <= 0:            
            raise PrecioVentaErrorExcepcion("Error: el sueldo no puede ser negativo o cero")

        if precio_venta > 999999:            
            raise PrecioVentaErrorExcepcion("Error: el precio es demasiado grande")
        
        if existencia < 0:
            raise ExistenciaErrorException("Error: no puede haber existencia menos a 0")
        
        self.nombre_producto = nombre_producto
        self.tipo = tipo
        self.precio_venta = precio_venta
        self.existencia = existencia



    @property
    def db(self):
        """Accede a la conexion global de la base de datos"""
        global pgdb
        if pgdb is None:
            raise DBException("La conexion a la base de datos no ha sido inicializada")
        return pgdb
    

       # Consultar los productos de la base de datos
    def consulta_productos():
        resultados  = []
     # Obtener una conexión
        with pgdb.get_cursor() as cursor:
                # Ejecutar una consulta
                cursor.execute("SELECT * FROM productos ORDER BY id_producto;")
                # Obtener los resultados
                filas = cursor.fetchall()
                # Mostrar los resultados
                for fila in filas:
                    print(fila)
                    resultados.append(fila)     

        return resultados
    
    def agregar_productos(self):
         with self.db.get_cursor() as cursor:
                cursor.execute("SET client_encoding TO 'UTF8';")                                                       
                cursor.execute("""INSERT INTO productos (nombre_producto, tipo, precio_venta, existencia)
                VALUES (%s, %s, %s, %s);""", (
                self.nombre_producto,
                self.tipo,
                self.precio_venta,
                self.existencia,
                ))
            
       
    
    @classmethod
    def buscar_producto(cls, id_producto):
        print("Buscando...")
        with pgdb.get_cursor() as cursor:
            cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
            fila = cursor.fetchall()
            print("Resultados ENCONTRADOS: ",fila)
            if not fila:
                print("No se encontró producto con el ID:", id_producto)
                raise AltaProductoError(f"No se encontró producto con el ID {id_producto}")
            print("Registro encontrado:", fila)
            return fila
                    
        
    @classmethod
    def buscar_producto_nombre(cls, nombre_producto):
        print("Buscando...")
        with pgdb.get_cursor() as cursor:  
                    cursor.execute("SELECT * FROM productos WHERE nombre_producto = %s;",(nombre_producto,))
                    fila = cursor.fetchall()
                    #fila = cursor.fetchone()
                    if not fila:  
                        print("No se encontró producto con la descripcion:", nombre_producto)
                        raise AltaProductoError(f"No se encontró producto con la descripcion {nombre_producto}")
                    #if fila is None:
                    #    print("No se encontró productos con el nombre:", nombre_producto)
                    #    return None

                    print("Registro encontrado:", fila)  
                    return fila

    @classmethod
    def eliminar_producto(cls, id_producto):
        with pgdb.get_cursor() as cursor:
                cursor.execute("SET client_encoding TO 'UTF8';")
                cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
       
           

    def modificar_producto(self, id_producto):
           with self.db.get_cursor() as cursor:
                cursor.execute("""UPDATE productos
                        SET nombre_producto = %s, tipo = %s, precio_venta =%s, existencia=%s
                        WHERE id_producto = %s""", (
                            self.nombre_producto, self.tipo,self.precio_venta,self.existencia, id_producto)
                )
                print("Producto modificado con éxito.")
        

    @staticmethod
    def descontar_existencia(id_producto, cantidad):
              with pgdb.get_cursor() as cursor:
                cursor.execute("SET client_encoding TO 'UTF8';")
                cursor.execute("UPDATE productos SET existencia = existencia - %s WHERE id_producto = %s", (cantidad, id_producto))  
      
      


    
class AltaProductoError(Exception):
    pass

class PrecioVentaErrorExcepcion(Exception):
    pass

class ExistenciaErrorException(Exception):
    pass
 

class DBException(Exception):
    pass



