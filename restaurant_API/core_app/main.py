from flask import Blueprint, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_login import login_required, current_user

from . import db
from .models import Restaurant
from .models import User
from .auth import token_required
# Vistas principales
main = Blueprint('main',__name__)

@main.route("/")
def index():
    return redirect(url_for("auth.login"))

@main.route("/profile")
@login_required
@token_required
def profile():
    #user = User.query.filter_by(correo = current_user.correo).first_or_404()
    #restaurantes = user.restaurantes  
    restaurantes = Restaurant.query.filter_by(user = current_user).order_by(Restaurant.fecha.desc()).all()
    
    ans = None
    
    if len(restaurantes) == 0:
        ans = "Saludos {}\nActualmente no tienes restaurantes registrados.".format(current_user.nombre)

    else:
        ans = "Saludos {}\nEstos son los restaurantes que tienes registrados: {}".format(current_user.nombre, restaurantes)

    return ans

# CRUD

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
    menu = request.json["menu"]
    telefono = request.json["telefono"]
    domicilio = request.json["domicilio"]

    restaurante = Restaurant(nombre = nombre, categoria = categoria, lugar = lugar, direccion = direccion, menu = menu, telefono = telefono,domicilio = domicilio == "True", user = current_user)
    db.session.add(restaurante)
    db.session.commit()
    
    return "{}, el restaurante {} ha sido agregado correctamente!!".format(current_user.nombre, nombre)

@main.route("/editar")
@login_required
def editar_restaurante():
    restaurantes = Restaurant.query.filter_by(user = current_user).order_by(Restaurant.fecha.desc()).all()
    
    ans = None
    
    if len(restaurantes) == 0:
        ans = "{}\nActualmente no tienes restaurantes registrados.".format(current_user.nombre)

    else:
        items = "\n"
        for res in restaurantes:
            #print(res,type(res))
            items += (str(res)+"\n\n")
        ans = "{}\nEstos son los restaurantes que tienes registrados: {}".format(current_user.nombre, items)

    return ans


@main.route("/editar", methods=['POST'])
@login_required
def editar_restaurante_post():
    nombre = request.json["nombre_antes"]
    ans = None
    restaurante = Restaurant.query.filter_by(user = current_user,nombre = nombre).first()
    band = False
    if not restaurante:
        ans = "No tienes ningún restaurante registrado con ese nombre!!"
    else:
        try:
            restaurante.nombre = request.json["nombre_despues"]
            band = True
        except:
            pass        
        try:
            restaurante.lugar = request.json["lugar"]
            band = True
        except:
            pass
            
        try:
            restaurante.direccion = request.json["direccion"]
            band = True
        except:
            pass
        try:
            restaurante.telefono = request.json["telefono"]
            band = True
        except:
            pass
        try:
            restaurante.domicilio = request.json["domicilio"]
            band = True
        except:
            pass
        if band:
            db.session.commit()
            ans = "Se actualizó el restaurante correctamente"
        else:
            ans = "Suministra algún campo para actualizar!!"
    return ans

@main.route("/eliminar")
@login_required
def eliminar_restaurante():
    return "Suministre el nombre del restaurante que desea borrar, campo : nombre"

@main.route("/eliminar", methods=['POST'])
@login_required
def eliminar_restaurante_post():
    nombre = request.json["nombre"]
    ans = None
    restaurante = Restaurant.query.filter_by(user = current_user,nombre = nombre).first()
    
    if not restaurante:
        ans = "No tienes ningún restaurante registrado con ese nombre!!"
    else:
        db.session.delete(restaurante)
        db.session.commit()

        ans = "Se eliminó el restaurante {} correctamente".format(nombre)

    return ans