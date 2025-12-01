from flask import Blueprint, render_template, redirect, url_for
from forms.auth_forms import LoginForm  # Importa tu formulario de login

welcome_bp = Blueprint('welcome', __name__)

@welcome_bp.route('/')
def index():
    return render_template('base.html')

@welcome_bp.route('/ingresar')
def ingresar():
    form = LoginForm()  # Crea una instancia del formulario
    return render_template('base.html', form=form)