
from psycopg2.pool import ThreadedConnectionPool
from contextlib import contextmanager

db_config = { "host" : "localhost",
                "database" : "sistema_ventas",
                "user" : "uacm",
                "password" : "12345"}

_tabla_usuarios = "CREATE TABLE usuarios(idVendedor SERIAL PRIMARY KEY,nombre TEXT,apellidoPaterno TEXT,apellidoMaterno TEXT,edad NUMERIC(10,2),perfil TEXT,comision NUMERIC(10,2),contrasenia TEXT,numero_telefono VARCHAR(15), sueldo INT);"

_tabla_productos= "CREATE TABLE productos(Id_producto SERIAL PRIMARY KEY,nombre_producto TEXT,tipo TEXT,precio_venta NUMERIC(10,2),existencia NUMERIC(10,2));"

_tabla_ventas= "CREATE TABLE ventas(idVenta SERIAL,nombre_producto TEXT,precio_venta TEXT,tipo TEXT,fecha_venta TEXT,cantidad_vendida NUMERIC(10,2),idVendedor INTEGER,descuento FLOAT,FOREIGN KEY (idVendedor) REFERENCES usuarios (idVendedor) ON UPDATE CASCADE);"

class PostgresDB:
    def __init__(self):
        self.app = None
        self.pool = None

    def init_app(self, app):
        self.app = app
        self.connect()

    def connect(self):
        self.pool = ThreadedConnectionPool(minconn=1, maxconn=30, **db_config)

    def create_all_tables_usuarios(self):
        drop_usuarios ="DROP TABLE IF EXISTS usuarios CASCADE;"
        with self.get_cursor() as cur: 
            cur.execute(drop_usuarios)
            cur.execute(_tabla_usuarios)

    def create_all_tables_productos(self):
        drop_productos ="DROP TABLE IF EXISTS productos;"
        with self.get_cursor() as cur: 
            cur.execute(drop_productos)
            cur.execute(_tabla_productos)

    def create_all_tables_vendedores(self): 
        drop_vendedores ="DROP TABLE IF EXISTS vendedores;"
        with self.get_cursor() as cur: 
            cur.execute(drop_vendedores)
            cur.execute(_tabla_vendedores)

    def create_all_tables_administradores(self):
        drop_administradores ="DROP TABLE IF EXISTS administradores;"
        with self.get_cursor() as cur: 
            cur.execute(drop_administradores)
            cur.execute(_tabla_administradores)

    def create_all_tables_ventas(self):
        drop_ventas ="DROP TABLE IF EXISTS ventas;"
        with self.get_cursor() as cur: 
            cur.execute(drop_ventas)
            cur.execute(_tabla_ventas)

    @contextmanager
    def get_cursor(self):
        if self.pool is None:
            self.connect()
        con = self.pool.getconn()
        try:
            yield con.cursor()
            con.commit()
        finally:
            self.pool.putconn(con)