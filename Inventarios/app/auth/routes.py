from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from . import auth_bp
from .forms import LoginForm
from app.models import Trabajador


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        trabajador = Trabajador.query.filter_by(dni=form.dni.data).first()

        if not trabajador or not check_password_hash(trabajador.password_hash, form.password.data):
            flash('DNI o contraseña incorrectos.', 'danger')
            return render_template('auth/login.html', form=form)

        if not trabajador.activo:
            flash('Tu cuenta está desactivada.', 'warning')
            return render_template('auth/login.html', form=form)

        login_user(trabajador)
        return redirect(url_for('main.dashboard'))

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))