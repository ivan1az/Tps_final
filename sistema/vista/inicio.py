from flask import Flask, request, redirect, url_for, render_template
from sistema.extencion.extencion import pgdb
from .views import registrar_rutas
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sistema.modelo.Persona import Persona
from sistema.modelo.Usuarios import Usuarios

# Datos de usuarios (simulados para el ejemplo)
USUARIOS = {
    'usuario1': 'u1',
    'usuario2': 'u2'
}


def create_app():
    app = Flask(__name__)
    registrar_rutas(app)

    return app

app = create_app()
pgdb.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)
    #app.run()


    usuario = Usuarios("Juan", "Pérez","Rodriguez", 30,"Administrador",0,"2345", "5512345678", 10000)