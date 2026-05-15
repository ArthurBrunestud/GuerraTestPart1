from .extensions import db
from flask_login import UserMixin


# ============================================================
# TABLAS MAESTRAS
# ============================================================

class Trabajador(UserMixin, db.Model):
    __tablename__ = 'mae_trabajadores'

    id            = db.Column(db.Integer, primary_key=True)
    dni           = db.Column(db.String(8), nullable=False, unique=True)
    nombre        = db.Column(db.String(80), nullable=False)
    apellido      = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    activo        = db.Column(db.Boolean, nullable=False, default=True)
    creado_en     = db.Column(db.DateTime, nullable=False, server_default=db.func.now())


class Proveedor(db.Model):
    __tablename__ = 'mae_proveedores'

    id        = db.Column(db.Integer, primary_key=True)
    nombre    = db.Column(db.String(150), nullable=False, unique=True)
    telefono  = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.Text, nullable=True)
    activo    = db.Column(db.Boolean, nullable=False, default=True)
    creado_en = db.Column(db.DateTime, nullable=False, server_default=db.func.now())


class Producto(db.Model):
    __tablename__ = 'mae_productos'

    id            = db.Column(db.Integer, primary_key=True)
    nombre        = db.Column(db.String(150), nullable=False, unique=True)
    descripcion   = db.Column(db.Text, nullable=True)
    categoria     = db.Column(db.String(80), nullable=False)
    marca         = db.Column(db.String(80), nullable=True)
    precio_compra = db.Column(db.Numeric(12, 2), nullable=False)
    moneda        = db.Column(db.String(10), nullable=False, default='PEN')
    stock         = db.Column(db.Integer, nullable=False, default=0)
    imagen_url    = db.Column(db.String(255), nullable=True)
    activo        = db.Column(db.Boolean, nullable=False, default=True)
    creado_en     = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    @property
    def disponible(self):
        return self.stock > 0

    movimientos = db.relationship('MovimientoStock', backref='producto', lazy=True)


# ============================================================
# TABLA TRANSACCIONAL
# ============================================================

class MovimientoStock(db.Model):
    __tablename__ = 'trs_movimientos_stock'

    id           = db.Column(db.Integer, primary_key=True)
    producto_id  = db.Column(db.Integer, db.ForeignKey('mae_productos.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('mae_proveedores.id'), nullable=True)
    tipo         = db.Column(db.String(10), nullable=False)
    cantidad     = db.Column(db.Integer, nullable=False)
    stock_despues= db.Column(db.Integer, nullable=False)
    notas        = db.Column(db.Text, nullable=True)
    fecha        = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    proveedor    = db.relationship('Proveedor', backref='movimientos', lazy=True)