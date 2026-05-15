from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from . import proveedores_bp
from .forms import ProveedorForm, EmptyForm
from ..models import Proveedor
from ..extensions import db


@proveedores_bp.route('/')
@login_required
def index():
    proveedores = Proveedor.query.order_by(Proveedor.nombre).all()  # todos, activos e inactivos
    form        = EmptyForm()
    return render_template('proveedores/index.html', proveedores=proveedores, form=form)


@proveedores_bp.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
    form = ProveedorForm()
    if form.validate_on_submit():
        existe = Proveedor.query.filter_by(nombre=form.nombre.data).first()
        if existe:
            flash('Ya existe un proveedor con ese nombre.', 'danger')
            return render_template('proveedores/form.html', form=form, titulo='Agregar proveedor')

        proveedor = Proveedor(
            nombre    = form.nombre.data,
            telefono  = form.telefono.data or None,
            direccion = form.direccion.data or None
        )
        db.session.add(proveedor)
        db.session.commit()
        flash('Proveedor registrado correctamente.', 'success')
        return redirect(url_for('proveedores.index'))

    return render_template('proveedores/form.html', form=form, titulo='Agregar proveedor')


@proveedores_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    proveedor = Proveedor.query.get_or_404(id)
    form      = ProveedorForm(obj=proveedor)

    if form.validate_on_submit():
        duplicado = Proveedor.query.filter(
            Proveedor.nombre == form.nombre.data,
            Proveedor.id     != proveedor.id
        ).first()
        if duplicado:
            flash('Ya existe otro proveedor con ese nombre.', 'danger')
            return render_template('proveedores/form.html', form=form, titulo='Editar proveedor')

        proveedor.nombre    = form.nombre.data
        proveedor.telefono  = form.telefono.data or None
        proveedor.direccion = form.direccion.data or None
        db.session.commit()
        flash('Proveedor actualizado correctamente.', 'success')
        return redirect(url_for('proveedores.index'))

    return render_template('proveedores/form.html', form=form, titulo='Editar proveedor')


@proveedores_bp.route('/<int:id>/activar', methods=['POST'])
@login_required
def activar(id):
    proveedor = Proveedor.query.get_or_404(id)
    proveedor.activo = True
    db.session.commit()
    flash(f'Proveedor "{proveedor.nombre}" activado.', 'success')
    return redirect(url_for('proveedores.index'))


@proveedores_bp.route('/<int:id>/desactivar', methods=['POST'])
@login_required
def desactivar(id):
    proveedor = Proveedor.query.get_or_404(id)
    proveedor.activo = False
    db.session.commit()
    flash(f'Proveedor "{proveedor.nombre}" desactivado.', 'warning')
    return redirect(url_for('proveedores.index'))