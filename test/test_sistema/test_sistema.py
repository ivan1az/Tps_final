import pytest
from sistema.vista.inicio import create_app
from sistema.extencion.extencion  import pgdb


#carga los metodos de las vistas

@pytest.fixture(scope="session")
def app_flask():
    # Setup de la aplicación 
    app = create_app()
    
    app.config.update({
        "TESTING": True,
    })

    # Inicialización de la base de datos
    print("...inicializando entorno de TESTING...")
    pgdb.init_app(app)
    #pgdb.create_all_tables()
 
    yield app
    # apartir de aquí se pone el código para liberar los recursos 
    # teardown limpiar/ reinicializar


# @pytest.fixture(scope="session")

# NOTA: Quitar el alcance de la fixture de "sesión" para que cada vez que se ejecute un test
# se cree un nuevo cliente y se limpie la sesión del usuario
@pytest.fixture
def client(app_flask):
    print("creando cliente...")
    client = app_flask.test_client()
    return client


#--------------------------------------------------
# Test de las transacciones de la aplicación
#--------------------------------------------------

def test_login(app_flask, client):
    with client:
        usuario = 'Juan'
        password = '8314'
        response = client.post("/login", data={"usuario":  usuario , "contrasena": password}, follow_redirects=True)
        data = response.get_data().decode('utf-8')
        msj_esperado = "Página de Inicio"
        assert msj_esperado in data
        assert response.status_code == 200