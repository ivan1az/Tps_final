from sistema.modelo.Persona import Persona, AltaPersonaEdadException, AltaPersonaNombreException
from sistema.extencion.extencion import pgdb 
 
class Usuarios(Persona):
    
    def __init__(self, nombre, apellidoPaterno, apellidoMaterno, edad, perfil, comision, contrasenia, numero_telefono,sueldo):
        super().__init__(nombre, apellidoPaterno, apellidoMaterno, edad)
        if isinstance(sueldo, str):
            try:
                sueldo = float(sueldo)
            except:
                raise  AltaUsuariosSueldoException("Error: el sueldo es inválido")
        
        if sueldo <= 0:            
            raise AltaUsuariosSueldoException("Error: el sueldo no puede ser negativo o cero")

        if sueldo > 99999:            
            raise AltaUsuariosSueldoException("Error: el precio es demasiado grande")
        
        if not contrasenia.strip():
            raise AltaUsuariosException("Error: el campo contrasenia no debe estar vacio")
        
        if comision < 0:
            raise AltaUsuariosException("Error: el campo comision no debe ser menor a 0")


        self.perfil = perfil
        self.comision = comision
        self.contrasenia = contrasenia
        self.numero_telefono = numero_telefono
        self.sueldo = sueldo

  
    @property
    def db(self):
        """Accede a la conexion global de la base de datos"""
        global pgdb
        if pgdb is None:
            raise DBException("La conexion a la base de datos no ha sido inicializada")
        return pgdb
    

      # Consultar los productos de la base de datos
    def consulta_usuarios():
        resultados  = []
        # Obtener una conexión
        with pgdb.get_cursor() as cursor:
          # Ejecutar una consulta
                cursor.execute("SELECT * FROM usuarios")
                # Obtener los resultados
                filas = cursor.fetchall()
                # Mostrar los resultados
                for fila in filas:
                    print(fila)
                    resultados.append(fila) 
        return resultados
    
    
    def agregar_usuarios(self):
        with self.db.get_cursor() as cursor:
                cursor.execute("SET client_encoding TO 'UTF8';")                                                                                             
                cursor.execute("""INSERT INTO usuarios(nombre, apellidoPaterno, apellidoMaterno, edad, perfil, comision, contrasenia, numero_telefono, sueldo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", (
                self.nombre,
                self.apellidoPaterno,
                self.apellidoMaterno,
                self.edad,
                self.perfil,
                self.comision,
                self.contrasenia,
                self.numero_telefono,
                self.sueldo
                ))
    

    @classmethod
    def buscar_usuario(cls,idVendedor):
        print("Buscando...")
        with pgdb.get_cursor() as cursor:  
            cursor.execute("SELECT * FROM usuarios WHERE idvendedor = %s", (idVendedor,))
            fila = cursor.fetchall()
                    #fila = cursor.fetchone()
            if not fila:
                print("No se encontró usuarios con el ID:", idVendedor)
                raise AltaUsuariosException("No se encontró usuarios con el ID:", idVendedor)
              
            print("Registro encontrado:", fila)  
            return fila
        
    @classmethod
    def buscar_usuario_por_nombre(cls, nombre):
        print("Buscando por nombre...")
        with pgdb.get_cursor() as cursor:  
            cursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (nombre,))
            fila = cursor.fetchall()
            if not fila:
                print("No se encontró usuarios con el nombre:", nombre)
                raise AltaUsuariosException("No se encontró usuarios con el nombre:", nombre)
              
            print("Registro encontrado:", fila)  
            return fila
        
       
    @classmethod
    def eliminar_usuario(cls, idVendedor):
        with pgdb.get_cursor() as cursor:
                cursor.execute("SET client_encoding TO 'UTF8';")
                cursor.execute("DELETE FROM usuarios WHERE idvendedor = %s", (idVendedor,))
        

    def modificar_vendedor(self, idVendedor):
        with self.db.get_cursor() as cursor:
                cursor.execute("""UPDATE usuarios
                        SET nombre = %s,  apellidopaterno = %s,  apellidomaterno = %s, edad = %s,perfil = %s,comision =%s,contrasenia=%s, numero_telefono = %s, sueldo=%s
                        WHERE idvendedor = %s""", (
                        self.nombre, self.apellidoPaterno, self.apellidoMaterno, self.edad, self.perfil, self.comision, self.contrasenia,self.numero_telefono,self.sueldo, idVendedor)
                )
                print("Vendedor modificado con éxito.")

       

class DBException(Exception):
    pass

class AltaUsuariosException(Exception):
    pass

class AltaUsuariosSueldoException(Exception):
    pass