from flask import session, flash, redirect, url_for, render_template, request
from flask import flash
from flask import session
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from datetime import datetime
from flask import make_response
import json
import csv
import io




#from modelo.Usuario import Usuario
from sistema.modelo.Venta import Venta
from sistema.modelo.Producto import Producto
from sistema.modelo.Usuarios import Usuarios,AltaUsuariosException

USUARIOS = {
    'usuario1': 'u1',
    'usuario2': 'u2'
}

def registrar_rutas(app):


    SECRET_KEY='2ca8efd458259a5de5d4c2ce5692475d31401923470d34b1b6b86055453b5488017858b6351e4bd8615e7cf669cdb63e170d792865c04846cb06e6aa48f82b7f'
    app.config['SECRET_KEY'] = SECRET_KEY
    
    
    @app.route('/', methods=['GET', 'POST'])
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['usuario']
            password = request.form['contrasena']
            msj = 'Credenciales incorrectas'
            if not username or not password:
                msj = 'Usuario o contraseña no pueden estar vacíos'
                flash(msj, 'danger')
                return render_template('login.html', error=msj), 401

            try:
                resultado = Usuarios.buscar_usuario_por_nombre(username)
            except AltaUsuariosException:
                
                flash(msj, 'danger')
                return render_template('login.html', error=msj), 401

            user_data = resultado[0]  
            password_bd = user_data[7] 

            if password == password_bd:
                session['usuario'] = username
                msj = "Bienvenido " + username
                flash(msj, 'success')
                return render_template('menu.html')
            else:
                flash(msj, 'danger')
                return render_template('login.html', error=msj), 401
        else:
            return render_template('login.html')
        
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session.clear()  
        msj = "Has cerrado la sesión correctamente"
        flash(msj, 'success')
        return  render_template('login.html')
        

    @app.route('/reporte_venta', methods=['GET', 'POST'])
    def consulta_Ventas():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login'))  
        resultados = Venta.consulta_ventas() 
        return render_template("reporte_venta.html", datos=resultados)
        
    @app.route('/descargar_reporte', methods=['POST'])
    def descargar_reporte():
        if 'usuario' not in session:
            flash('No se ha iniciado sesión', 'danger')
            return redirect(url_for('login'))

        datos = Venta.consulta_ventas()  # Asume que devuelve una lista de tuplas

        # Crear respuesta tipo CSV
        output = []
        output.append([
            "ID Venta", "Nombre Producto", "Precio Venta", "Tipo",
            "Fecha Venta", "Cantidad Vendida", "ID Vendedor", "Descuento"
        ])

        for fila in datos:
            output.append(list(fila))

        # Generar respuesta como archivo
        si = io.StringIO()
        writer = csv.writer(si)
        writer.writerows(output)

        response = make_response(si.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=reporte_ventas.csv'
        response.headers['Content-Type'] = 'text/csv'

        return response
    
    
    @app.route('/usuarios', methods=['GET', 'POST'])
    def usuarios():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login'))
        resultados = Usuarios.consulta_usuarios()
        return render_template("usuarios.html", datos=resultados)
        
    @app.route('/menu', methods=['GET', 'POST'])
    def menu():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login'))  
        return render_template('menu.html')
    

    @app.route('/agregar_usuarios', methods=['GET', 'POST'])
    def agregar_usuarios():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login'))  
        
        if request.method == 'POST':
            print(request.form)
            
            nombre = request.form['nombre']
            apellido_paterno = request.form['apellido_paterno']
            apellido_materno = request.form['apellido_materno']
            edad = int(request.form['edad'])
            perfil = request.form['perfil']
            comision = float(request.form['comision'])
            numero_telefono = request.form['numero_telefono']
            contrasenia = request.form['contrasenia']
            sueldo = float(request.form['sueldo'])

            try:
                print("Creando un vendedor...")
                usuario = Usuarios(nombre, apellido_paterno, apellido_materno, edad, perfil, comision,contrasenia,numero_telefono,sueldo)
                usuario.agregar_usuarios()

                msj= "El empleado se dio de alta correctamente"
                flash(msj, 'success')
                return  render_template('agregar_usuarios.html')
            
            except Exception as e:
                msj= "Error al dar de alta el empleado"
                flash(msj, 'danger')
                return render_template('agregar_usuarios.html', error = msj), 401
        else:
            return render_template('agregar_usuarios.html')

    @app.route('/eliminar_usuario', methods=['GET', 'POST'])
    def eliminar_usuario():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login'))
        
        if request.method == 'POST':
            id_empleado = request.form['id_empleado'] 
            try:
                print("Intentando localizar usuario", id_empleado)
                id_empleado = int(id_empleado)
                result = Usuarios.buscar_usuario(id_empleado)
               
                if result != None:
                    print("Usuario localizado", result)
                    Usuarios.eliminar_usuario(id_empleado)
                else:
                    print("No existe un usuario con ese ID.")
                    msj = "No existe un usuario con ese ID."
                    
                msj= "El empleado se eliminó correctamente"
                flash(msj, 'success')
                return render_template('eliminar_usuario.html')
            except Exception as e:
                msj= "Error al eliminar el empleado"
                flash(msj, 'danger')
                return render_template('eliminar_usuario.html', error = msj), 401
        else:
            return render_template('eliminar_usuario.html')
        
    @app.route('/buscar_usuario', methods=['GET', 'POST'])
    def buscar_usuario():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login'))

        if request.method == 'POST':
            try:
                id_usuario = request.form['id_usuario']
                result = Usuarios.buscar_usuario(id_usuario)
                if result:
                    print("Vendedor encontrado:", result)
                    session['id_usuario'] = id_usuario
                    return redirect(url_for('modificar_usuario'))
                else:
                    print("No existe un usuario con ese ID.")
                    msj= "No existe un usuario con ese ID"
                    flash(msj, 'danger')
                    return render_template('buscar_usuario.html', error = msj), 401
            except Exception as e:
                msj= "Error al encontrar el empleado"
                flash(msj, 'danger')
                return render_template('buscar_usuario.html', error = msj), 401
        else:
            return render_template('buscar_usuario.html')

    @app.route('/modificar_usuario', methods=['GET', 'POST'])
    def modificar_usuario():
        if 'usuario' not in session:
            flash('No se ha iniciado sesión', 'danger')
            return redirect(url_for('login'))

        id_usuario = session.get('id_usuario')

        if not id_usuario:  
            flash('No se encontró el usuario', 'danger')
            return redirect(url_for('buscar_usuario'))

        print(f"Modificando usuario con ID: {id_usuario}")

        if request.method == 'POST':
            nombre = request.form['nombre']
            apellido_paterno = request.form['apellido_paterno']
            apellido_materno = request.form['apellido_materno']
            edad = int(request.form['edad'])
            perfil = request.form['perfil']
            comision = float( request.form['comision'])
            numero_telefono = request.form['numero_telefono']
            contrasenia = request.form['contrasenia']
            sueldo = float(request.form['sueldo'])

            try:
                print("Buscando vendedor...")
                usuario = Usuarios(nombre,apellido_paterno,apellido_materno,edad,perfil,comision, contrasenia,numero_telefono, sueldo)
                usuario.modificar_vendedor(id_usuario)
                print("Usuario modificado con exito")
                flash("El empleado se modificó correctamente", "success")
                return redirect(url_for('buscar_usuario'))

            except Exception as e:
                flash(f"Error al modificar el usuario: {str(e)}", "danger")
                return redirect(url_for('buscar_usuario'))

        return render_template('modificar_usuario.html')
    
#---------------------------------------------------------------------------------------------------#
#endpoints de productos

    @app.route('/consulta_inventario', methods=['GET', 'POST'])
    def consulta_Inventario():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login')) 
        resultados = Producto.consulta_productos() 
        print("Datos obtenidos:", resultados)
        return render_template("consulta_inventario.html", datos=resultados)
    

    @app.route('/agregar_productos', methods=['GET', 'POST'])
    def agregar_productos():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login'))  
        
        if request.method == 'POST':
            print(request.form)
            
            nombre_producto = request.form['nombre_producto']
            tipo = request.form['tipo']
            precio_venta = float(request.form['precio_venta'])
            existencia = int(request.form['existencia'])

            try:
                print("Creando un producto...")
                producto = Producto(nombre_producto,tipo,precio_venta,existencia)
                print("Producto introducido", producto)
                producto.agregar_productos()

                msj= "El producto se dio de alta correctamente"
                flash(msj, 'success')
                return  render_template('agregar_productos.html')
            
            except Exception as e:
                msj= "Error al dar de alta el producto"
                print("Error al agregar producto:", str(e))
                flash(msj, 'danger')
                return render_template('agregar_productos.html', error = msj), 401
        else:
            return render_template('agregar_productos.html')

    
    @app.route('/eliminar_producto', methods=['GET', 'POST'])
    def eliminar_producto():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login'))
        
        if request.method == 'POST':
            id_producto = request.form['id_producto'] 
            try:
                print("Intentando localizar producto", id_producto)
                id_producto = int(id_producto)
                result = Producto.buscar_producto(id_producto)
               
                if result != None:
                    print("Producto localizado", result)
                    Producto.eliminar_producto(id_producto)
                else:
                    print("No existe un producto con ese ID.")
                    msj = "No existe un producto con ese ID."
                    
                msj= "El producto se eliminó correctamente"
                flash(msj, 'success')
                return render_template('eliminar_producto.html')
            except Exception as e:
                msj= "Error al eliminar el producto"
                flash(msj, 'danger')
                return render_template('eliminar_producto.html', error = msj), 401
        else:
            return render_template('eliminar_producto.html')
       
    @app.route('/buscar_producto', methods=['GET', 'POST'])
    def buscar_producto():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login'))

        if request.method == 'POST':
            try:
                id_producto = request.form['id_producto']
                result = Producto.buscar_producto(id_producto)
                if result:
                    print("Vendedor encontrado:", result)
                    session['id_producto'] = id_producto
                    return redirect(url_for('modificar_producto'))
                else:
                    print("No existe un producto con ese ID.")
                    msj= "No existe un producto con ese ID"
                    flash(msj, 'danger')
                    return render_template('buscar_usuario.html', error = msj), 401
            except Exception as e:
                msj= "Error al encontrar el producto"
                flash(msj, 'danger')
                return render_template('buscar_producto.html', error = msj), 401
        else:
            return render_template('buscar_producto.html')
        
    @app.route('/modificar_producto', methods=['GET', 'POST'])
    def modificar_producto():
        if 'usuario' not in session:
            flash('No se ha iniciado sesión', 'danger')
            return redirect(url_for('login'))

        id_producto = session.get('id_producto')

        if not id_producto:  
            flash('No se encontró el producto', 'danger')
            return redirect(url_for('buscar_producto'))

        print(f"Modificando producto con ID: {id_producto}")

        if request.method == 'POST':
            
            nombre_producto = request.form['nombre_producto']
            tipo = request.form['tipo']
            precio_venta = float(request.form['precio_venta'])
            existencia = int (request.form['existencia'])
            try:
                print("Buscando producto...")
                producto = Producto(nombre_producto,tipo,precio_venta,existencia)
                producto.modificar_producto(id_producto)
            
                print("Producot modificado con exito")
                flash("El producto se modificó correctamente", "success")
                return redirect(url_for('buscar_producto'))

            except Exception as e:
                flash(f"Error al modificar el usuario: {str(e)}", "danger")
                return redirect(url_for('buscar_producto'))

        return render_template('modificar_producto.html')
    
#-------------------------------------------------------------------------#
#endpoints de venta


    @app.route('/agregar_venta', methods=['GET', 'POST'])
    def agregar_venta():
        if 'usuario' not in session:
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect(url_for('login'))

        if request.method == 'POST':
            try:
                print(request.form)

                productos_json = request.form['productos']
                productos = json.loads(productos_json) 

                fecha_venta = request.form['fecha_venta']
                idvendedor = request.form['idvendedor']
                nacionalidad = request.form['Nacionalidad']
                
                try:
                    result = Usuarios.buscar_usuario(idvendedor)
                except AltaUsuariosException:
                    flash("No existe un vendedor con ese ID", 'danger')
                    return render_template('agregar_venta.html'), 401
                
                usuario = result[0]

                if usuario[5] != "Vendedor":
                    flash("El ID del empleado no es de un Vendedor", 'danger')
                    return render_template('agregar_venta.html'), 401
                
                for prod in productos:
                    nombre_producto = prod['nombre']
                    precio_venta = float(prod['precio'])
                    tipo = prod['talla']
                    cantidad_vendida = int(prod['cantidad'])

                    try:
                        res = Producto.buscar_producto_nombre(nombre_producto)
                        producto = res[0]
                    except:
                        flash(f"No existe un producto con el nombre: {nombre_producto}", 'danger')
                        return render_template('agregar_venta.html')

                    id_producto = producto[0]      
                    existencia_actual = producto[4]  
           
                    if cantidad_vendida > existencia_actual:
                        flash(f"No hay suficiente stock para '{nombre_producto}'. Solo quedan {existencia_actual}.", 'danger')
                        return render_template('agregar_venta.html')

                    if precio_venta >= 1000:
                        descuento = 0.10 if nacionalidad in ["Mexicana", "Estado Unidense", "Canadiense"] else 0.05
                    else:
                        descuento = 0

                    precio_descuento = (precio_venta * cantidad_vendida) * descuento
                    precio_total = (precio_venta * cantidad_vendida) - precio_descuento

                    
                    venta = Venta(nombre_producto, tipo, precio_total, 0, fecha_venta, cantidad_vendida, descuento)
                    venta.agregar_venta(idvendedor)

                    Producto.descontar_existencia(id_producto, cantidad_vendida)
                    print(f"Venta registrada y stock actualizado para {nombre_producto}")


                flash("Se generó la venta correctamente", 'success')
                return render_template('agregar_venta.html')

            except Exception as e:
                print("Error general:", str(e))
                flash("Error al realizar la venta", 'danger')
                return render_template('agregar_venta.html'), 401

        return render_template('agregar_venta.html')
