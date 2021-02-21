from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from werkzeug.utils import redirect, secure_filename
from flask_login import login_required, current_user

import os
from . import db
from .models import Restaurant
from .models import User
from .auth import token_required
# Vistas principales
main = Blueprint('main',__name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/profile")
@login_required
#@token_required
def profile():
    #user = User.query.filter_by(correo = current_user.correo).first_or_404()
    #restaurantes = user.restaurantes  
    restaurantes = Restaurant.query.filter_by(user = current_user).order_by(Restaurant.fecha.desc()).all()
    band = True if len(restaurantes) == 0 else  False
    return render_template("profile.html", name = current_user.nombre, band = band, restaurantes = restaurantes)


# CRUD
@main.route("/agregar_restaurante")
@login_required
def agregar_restaurante():
    #return "Pagina para agregar resturante, envie su peticion con los campos: nombre, categoria, lugar, direccion, telefono y domicilio"
    return render_template("agregar_restaurante.html")


@main.route("/agregar_restaurante", methods = ["POST"])
@login_required
def agregar_restaurante_post():
    nombre = request.form["nombre"]
    categoria = request.form["categoria"] 
    lugar = request.form["lugar"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    domicilio = False if request.form['options'] == "no" else True

    # obtenemos el archivo del input "archivo"
    f = request.files['logo']
    f2 = request.files['menu']
    filename = secure_filename(f.filename)
    filename2 = secure_filename(f2.filename)
    # Guardamos el archivo en el directorio "Archivos PDF"
    f.save(os.path.join("/home/juan/Documents/tec_emergentes/restaurant_API_front/core_app/static", filename))
    f2.save(os.path.join("/home/juan/Documents/tec_emergentes/restaurant_API_front/core_app/static", filename2))
    # Retornamos una respuesta satisfactoria
    logo_url = filename
    menu_url = filename2

    restaurante = Restaurant(nombre = nombre, categoria = categoria, lugar = lugar, direccion = direccion, telefono = telefono,domicilio = domicilio, user = current_user,logo_url = logo_url, menu_url = menu_url)
    db.session.add(restaurante)
    db.session.commit()
    
    return redirect(url_for("main.profile"))

@main.route("/detalles/<int:rest_id>/", methods=['GET'])
@login_required
def detalles(rest_id):
    restaurante = Restaurant.query.filter_by(id = rest_id).first()
    return render_template("detalle.html", restaurante = restaurante)


@main.route("/editar/<int:rest_id>/update", methods=['GET'])
@login_required
def editar_restaurante(rest_id):
    restaurante = Restaurant.query.filter_by(id = rest_id).first()
    return render_template("editar.html", restaurante = restaurante)


@main.route("/editar/<int:rest_id>/update", methods=['POST'])
@login_required
def editar_restaurante_post(rest_id):
    restaurante = Restaurant.query.filter_by(id = rest_id).first()


    restaurante.nombre = request.form["nombre"]
    restaurante.categoria = request.form["categoria"] 
    restaurante.lugar = request.form["lugar"]
    restaurante.direccion = request.form["direccion"]
    restaurante.telefono = request.form["telefono"]
    restaurante.domicilio = False if request.form['options'] == "no" else True


    # obtenemos el archivo del input "archivo"
    f = request.files['logo']
    f2 = request.files['menu']
    filename = secure_filename(f.filename)
    filename2 = secure_filename(f2.filename)
    # Guardamos el archivo en el directorio "Archivos PDF"
    if len(filename):
        f.save(os.path.join("/home/juan/Documents/tec_emergentes/restaurant_API_front/core_app/static", filename))
        restaurante.logo_url = filename
    if len(filename2):
        f2.save(os.path.join("/home/juan/Documents/tec_emergentes/restaurant_API_front/core_app/static", filename2))
        restaurante.menu_url = filename2

    db.session.commit()

    return redirect(url_for("main.profile"))


@main.route("/eliminar/<int:rest_id>/update", methods=['GET'])
@login_required
def eliminar_restaurante(rest_id):
    restaurante = Restaurant.query.filter_by(id = rest_id).first()
    db.session.delete(restaurante)
    db.session.commit()
    
    return redirect(url_for("main.profile"))
