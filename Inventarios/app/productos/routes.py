import io
import os
import unicodedata
from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename

from . import productos_bp
from .forms import ProductoForm, DesactivarForm
from app.extensions import db
from app.models import Producto


# ── Configuración de seguridad de imagen ──────────────────────────────────────
EXTENSIONES_PERMITIDAS   = {'jpg', 'jpeg', 'png'}
FORMATOS_PILLOW_PERMITIDOS = {'JPEG', 'PNG', 'WEBP'}
TAMANIO_MAXIMO_MB        = 2
TAMANIO_MAXIMO           = TAMANIO_MAXIMO_MB * 1024 * 1024


# ── Helpers ───────────────────────────────────────────────────────────────────
def limpiar_nombre(texto):
    normalizado = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in normalizado if not unicodedata.combining(c))


def extension_valida(filename):
    if '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS


def tamanio_valido(archivo):
    archivo.seek(0, 2)
    tamanio = archivo.tell()
    archivo.seek(0)
    return tamanio <= TAMANIO_MAXIMO


def contenido_valido(archivo):
    """
    Usa Pillow para decodificar el archivo completo.
    Detecta scripts o basura disfrazados con header de imagen válido.
    """
    try:
        datos = archivo.read()
        archivo.seek(0)

        img = Image.open(io.BytesIO(datos))
        img.verify()                              # Valida estructura y chunks

        if img.format not in FORMATOS_PILLOW_PERMITIDOS:
            return False

        img2 = Image.open(io.BytesIO(datos))
        img2.load()                               # Decodifica todos los píxeles

        return True
    except (UnidentifiedImageError, Exception):
        return False


def guardar_imagen(archivo, nombre_producto):
    if not extension_valida(archivo.filename):
        raise ValueError(f'Formato no permitido. Solo: {", ".join(EXTENSIONES_PERMITIDAS)}.')

    if not tamanio_valido(archivo):
        raise ValueError(f'El archivo supera el límite de {TAMANIO_MAXIMO_MB} MB.')

    if not contenido_valido(archivo):
        raise ValueError('El archivo no es una imagen válida.')

    extension      = archivo.filename.rsplit('.', 1)[1].lower()
    nombre_limpio  = limpiar_nombre(nombre_producto).strip().lower().replace(' ', '_')
    nombre_archivo = secure_filename(f"{nombre_limpio}.{extension}")
    ruta           = os.path.join(current_app.root_path, 'static', 'uploads', nombre_archivo)
    archivo.save(ruta)
    return nombre_archivo


# ── Rutas ─────────────────────────────────────────────────────────────────────
@productos_bp.route('/productos')
@login_required
def listar():
    productos       = Producto.query.all()   # todos, activos e inactivos
    form_desactivar = DesactivarForm()
    return render_template('productos/lista.html', productos=productos, form_desactivar=form_desactivar)


@productos_bp.route('/productos/<int:id>/activar', methods=['POST'])
@login_required
def activar(id):
    producto = Producto.query.get_or_404(id)
    producto.activo = True
    db.session.commit()
    flash(f'Producto "{producto.nombre}" activado.', 'success')
    return redirect(url_for('productos.listar'))

@productos_bp.route('/productos/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    form = ProductoForm()
    if form.validate_on_submit():
        existe = Producto.query.filter_by(nombre=form.nombre.data).first()
        if existe:
            flash('Ya existe un producto con ese nombre.', 'danger')
            return render_template('productos/registrar.html', form=form)

        imagen_url = None
        if form.imagen.data:
            try:
                imagen_url = guardar_imagen(form.imagen.data, form.nombre.data)
            except ValueError as e:
                flash(str(e), 'danger')
                return render_template('productos/registrar.html', form=form)

        producto = Producto(
            nombre        = form.nombre.data,
            descripcion   = form.descripcion.data,
            categoria     = form.categoria.data,
            marca         = form.marca.data,
            precio_compra = form.precio_compra.data,
            moneda        = form.moneda.data,
            stock         = form.stock.data,
            imagen_url    = imagen_url
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto registrado exitosamente.', 'success')
        return redirect(url_for('productos.listar'))

    return render_template('productos/registrar.html', form=form)


@productos_bp.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    producto = Producto.query.get_or_404(id)
    form     = ProductoForm(obj=producto)           # Precarga todos los campos

    if form.validate_on_submit():
        # Nombre duplicado en otro producto
        duplicado = Producto.query.filter(
            Producto.nombre == form.nombre.data,
            Producto.id     != producto.id
        ).first()
        if duplicado:
            flash('Ya existe otro producto con ese nombre.', 'danger')
            return render_template('productos/editar.html', form=form, producto=producto)

        # Reemplazar imagen solo si se sube una nueva
        if form.imagen.data:
            try:
                producto.imagen_url = guardar_imagen(form.imagen.data, form.nombre.data)
            except ValueError as e:
                flash(str(e), 'danger')
                return render_template('productos/editar.html', form=form, producto=producto)

        producto.nombre        = form.nombre.data
        producto.descripcion   = form.descripcion.data
        producto.categoria     = form.categoria.data
        producto.marca         = form.marca.data
        producto.precio_compra = form.precio_compra.data
        producto.moneda        = form.moneda.data
        producto.stock         = form.stock.data

        db.session.commit()
        flash('Producto actualizado exitosamente.', 'success')
        return redirect(url_for('productos.listar'))

    return render_template('productos/editar.html', form=form, producto=producto)


@productos_bp.route('/productos/<int:id>/desactivar', methods=['POST'])
@login_required
def desactivar(id):
    producto = Producto.query.get_or_404(id)
    producto.activo = False
    db.session.commit()
    flash(f'Producto "{producto.nombre}" desactivado.', 'warning')
    return redirect(url_for('productos.listar'))