from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from flask_session import Session
from package_model import controlador
import plotly.express as px
import pandas as pd

app=Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Puedes cambiar este tipo de almacenamiento según tus necesidades
Session(app)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/viviendas')
def viviendas():
    return render_template('sitio/viviendas.html')

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/admin/')
def admin_index():
    usuario = session.get('usuario', None)
    if usuario is None:
        return redirect(url_for('admin_login'))
    return render_template('admin/index.html')

@app.route('/admin/cerrar')
def cerrar():
    session['usuario'] = None
    return redirect(url_for('admin_login'))

@app.route('/admin/login', methods = ['get', 'post'])
def admin_login():
    if request.method == 'POST':
        usuario = controlador.buscarUsuario(request.form.get('txtUsuario'))
        if usuario is not None:
            if usuario[1] == request.form.get('txtPassword'):
                session['usuario'] = usuario
                return redirect(url_for('admin_index'))
            else:
                return '''<script>
                    alert("Contraseña incorrecta");
                    window.location.href = "/admin/login";
                </script>'''
        else:
            return '''<script>
                    alert("Usuario inexistente");
                    window.location.href = "/admin/login";
                </script>'''
    usuario = session.get('usuario', None)
    if usuario is None:
        return render_template('admin/login.html')
    else:
        return redirect(url_for('admin_index'))


@app.route('/admin/viviendas')
def admin_viviendas():
    usuario = session.get('usuario', None)
    if usuario is None:
        return redirect(url_for('admin_login'))
    viviendas = controlador.listarViviendas()
    if viviendas is None:
        viviendas = []
    localidades = controlador.listarLocalidades()
    return render_template("admin/viviendas.html", viviendas = viviendas, localidades = localidades)

@app.route('/admin/viviendas/guardar', methods = ['post'])
def guardarVivienda():
    nombre = request.form.get('txtNombre')
    imagen = request.files['txtImagen']
    location = request.form.get('txtLocacion')
    
    controlador.guardarVivienda(nombre, imagen.filename, location)
    return '''<script>
        alert("guardado correctamente")
        window.location.href="/admin/viviendas"
    </script>'''

@app.route('/admin/viviendas/eliminar', methods=['post'])
def eliminarVivienda():
    id = request.form.get('id')
    controlador.eliminarVivienda(id)
    return '''<script>
        alert("eliminado correctamente")
        window.location.href="/admin/viviendas"
    </script>'''

@app.route('/admin/habitantes')
def habitantes():
    usuario = session.get('usuario', None)
    if usuario is None:
        return redirect(url_for('admin_login'))
    habitantes = controlador.listarHabitantes()
    if habitantes is None:
        habitantes = []
    viviendas = controlador.listarViviendas()
    if viviendas is None:
        viviendas = []
    return render_template('/admin/habitantes.html', habitantes = habitantes, viviendas = viviendas)

@app.route('/admin/habitantes/guardar', methods=['POST'])
def guardarHabitante():
    nombre = request.form.get('txtNombre')
    sexo = request.form.get('txtSexo')
    direccion = request.form.get('txtVivienda')
    telefono = request.form.get('txtTelefono')
    ciudad = request.form.get('txtCiudad')
    controlador.guardarHabitante(nombre, sexo, direccion, telefono, ciudad)
    return '''<script>
        alert("Habitante guardado correctamente")
        window.location.href="/admin/habitantes"
    </script>'''

@app.route('/admin/habitantes/eliminar', methods=['POST'])
def eliminarHabitante():
    id = request.form.get('id')
    controlador.eliminarHabitante(id)
    return '''<script>
        alert("Habitante eliminado correctamente")
        window.location.href="/admin/habitantes"
    </script>'''

@app.route('/admin/dashboard')
def dashboard():
    data = controlador.listarLocalidades()
    for dat in data:
        if dat.get('habitantes') is None:
            dat['habitantes'] = 0
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Localidad', y='habitantes', title='Cantidad de Habitantes por Localidad')
    graph_html = fig.to_html(full_html=False)
    return render_template("admin/dashboard.html", fig=graph_html)

if __name__ =='__main__':
    app.run(debug=True)