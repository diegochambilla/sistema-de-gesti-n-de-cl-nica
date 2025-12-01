from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from database import db
from models.usuario_model import Usuario
from forms.auth_forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario and check_password_hash(usuario.password, form.password.data):
            if usuario.activo:
                login_user(usuario)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('admin.dashboard'))
            else:
                flash('Cuenta desactivada', 'danger')
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            rol=form.rol.data
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('usuario.index'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('welcome.index'))  # Redirigir explícitamente al welcome