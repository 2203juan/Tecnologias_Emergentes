from flask import Blueprint, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_login import login_required, current_user

from . import db
from .models import Restaurant
from .models import User

main = Blueprint('main',__name__)

@main.route("/")
def index():
    return "index"

@main.route("/profile")
@login_required
def profile():
    #user = User.query.filter_by(correo = current_user.correo).first_or_404()
    #restaurantes = user.restaurantes  
    restaurantes = Restaurant.query.filter_by(user = current_user).order_by(Restaurant.fecha.desc()).all()
    return "Saludos {}\nEstos son los restaurantes que tienes registrados: {}".format(current_user.nombre, restaurantes)

@main.route("/agregar_restaurante")
@login_required
def agregar_restaurante():
    return "Pagina para agregar resturante, envie su peticion con los campos: nombre, categoria, lugar, direccion, telefono y domicilio"

@main.route("/agregar_restaurante", methods = ["POST"])
@login_required
def agregar_restaurante_post():
    nombre = request.json["nombre"]
    categoria = request.json["categoria"]
    lugar = request.json["lugar"]
    direccion = request.json["direccion"]
    telefono = request.json["telefono"]
    domicilio = request.json["domicilio"]

    restaurante = Restaurant(nombre = nombre, categoria = categoria, lugar = lugar, direccion = direccion, telefono = telefono,domicilio = domicilio == "True", user = current_user)
    db.session.add(restaurante)
    db.session.commit()
    
    return "{}, el restaurante {} ha sido agregado correctamente!!".format(current_user.nombre, nombre)
