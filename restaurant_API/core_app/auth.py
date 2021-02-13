from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, logout_user, login_required, current_user

from .models import User
from . import db

import jwt
import datetime

from functools import wraps


auth = Blueprint("auth",__name__)

@auth.route("/registro")
def registro():
    return "Endpoint de Registro, envie su peticion con los campos: nombre,correo y clave"

@auth.route("/registro", methods = ["POST"])
def registro_post():
    nombre = request.json["nombre"]
    correo = request.json["correo"]
    clave = request.json["clave"]

    user = User.query.filter_by(correo = correo).first()

    if user:
        return "Este usuario ya está registrado"
    else:
        nuevo_usuario = User(correo = correo, nombre = nombre, clave = generate_password_hash(clave, method = "sha256"))
        db.session.add(nuevo_usuario)
        db.session.commit()
        return "Felicidades {}, ya te registraste!!".format(nombre)


@auth.route("/login")
def login():
    return "Endpoint de Login, envie su peticion con los campos: correo y clave"

@auth.route("/login", methods = ["POST"])
def login_post():
    correo = request.json["correo"]
    clave = request.json["clave"]

    user = User.query.filter_by(correo = correo).first()

    if not user or not check_password_hash(user.clave, clave):
        return "Correo o contraseña no validos, por favor verifique"

    else:
        login_user(user)
        token = jwt.encode({'user': user.nombre,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 5)}, "secret_key")

        return token

# JWT FUNCTIONS

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return "Falta el token!!, ingresalo despues de la ruta; ruta?token = xxxxx", 403
        
        try:
            data = jwt.decode(token, "secret_key")

        except:
            return "Token no válido!!",403

        return f(*args, **kwargs) 
    return decorated

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logout exitoso"
