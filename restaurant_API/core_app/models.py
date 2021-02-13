from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    correo = db.Column(db.String(100), unique = True)
    clave = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    restaurantes = db.relationship("Restaurant",backref="user")


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    categoria = db.Column(db.String(100), nullable = False)
    lugar = db.Column(db.String(100), nullable = False)
    direccion = db.Column(db.String(100), nullable = False)
    menu = db.Column(db.Text(), nullable = False)
    telefono = db.Column(db.String(20), nullable = False)
    domicilio = db.Column(db.Boolean, nullable = False)
    fecha = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)   
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    def __repr__(self) -> str:
        info  = "Nombre: {},Categoria: {}, Lugar: {}, Direccion: {},Menú: {},Teléfono: {},Domicilio:{}".format(self.nombre, self.categoria, self.lugar, self.direccion, self.menu,
        self.telefono, "Si" if self.domicilio == True else "No")
        return info