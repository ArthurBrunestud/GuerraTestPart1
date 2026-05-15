from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from . import inventario_bp
from .forms import MovimientoForm
from ..models import Producto, Proveedor, MovimientoStock
from ..extensions import db

@inventario_bp.route('/')
@login_required
def index():
    movimientos = MovimientoStock.query\
        .order_by(MovimientoStock.fecha.desc())\
        .all()
    return render_template('inventario/index.html', movimientos=movimientos)

@inventario_bp.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    form = MovimientoForm()

    form.producto_id.choices = [
        (p.id, p.nombre) for p in Producto.query.filter_by(activo=True).order_by(Producto.nombre).all()
    ]
    form.proveedor_id.choices = [(0, '— Selecciona un proveedor —')] + [
        (p.id, p.nombre) for p in Proveedor.query.filter_by(activo=True).order_by(Proveedor.nombre).all()
    ]

    if form.validate_on_submit():
        # Proveedor obligatorio solo en entradas
        if form.tipo.data == 'entrada' and form.proveedor_id.data == 0:
            flash('Las entradas requieren un proveedor.', 'danger')
            return render_template('inventario/form.html', form=form)

        producto = Producto.query.get_or_404(form.producto_id.data)
        cantidad = form.cantidad.data

        if form.tipo.data == 'salida':
            if producto.stock == 0:
                flash(f'"{producto.nombre}" no tiene stock disponible.', 'danger')
                return render_template('inventario/form.html', form=form)
            if cantidad > producto.stock:
                flash(f'Stock insuficiente. Stock actual: {producto.stock}', 'danger')
                return render_template('inventario/form.html', form=form)

        if form.tipo.data == 'entrada':
            producto.stock += cantidad
        else:
            producto.stock -= cantidad

        # En salidas el proveedor queda como None
        proveedor_id = form.proveedor_id.data if (form.tipo.data == 'entrada' and form.proveedor_id.data != 0) else None

        movimiento = MovimientoStock(
            producto_id   = producto.id,
            proveedor_id  = proveedor_id,
            tipo          = form.tipo.data,
            cantidad      = cantidad,
            stock_despues = producto.stock,
            notas         = form.notas.data or None
        )
        db.session.add(movimiento)
        db.session.commit()
        flash('Movimiento registrado correctamente.', 'success')
        return redirect(url_for('inventario.index'))

    return render_template('inventario/form.html', form=form)