from flask import Flask, request, redirect, url_for
from database import db
from flask_login import LoginManager
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///saludplus.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clave-secreta-muy-segura-aqui"

# Inicializar la base de datos
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

# Configurar el loader de usuario
from models.usuario_model import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Importar y registrar blueprints después de inicializar la db y login_manager
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.usuario_controller import usuario_bp
from controllers.medico_controller import medico_bp
from controllers.paciente_controller import paciente_bp
from controllers.especialidad_controller import especialidad_bp
from controllers.cita_controller import cita_bp
from controllers.consulta_controller import consulta_bp
from controllers.receta_controller import receta_bp
from controllers.servicio_controller import servicio_bp
from controllers.factura_controller import factura_bp
from controllers.configuracion_controller import configuracion_bp
from controllers.welcome_controller import welcome_bp

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(medico_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(especialidad_bp)
app.register_blueprint(cita_bp)
app.register_blueprint(consulta_bp)
app.register_blueprint(receta_bp)
app.register_blueprint(servicio_bp)
app.register_blueprint(factura_bp)
app.register_blueprint(configuracion_bp)
app.register_blueprint(welcome_bp)

@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return dict(is_active=is_active)

@app.route("/")
def home():
    return redirect(url_for('auth.login'))
@app.route('/')
def index():
    return redirect(url_for('welcome.index'))

# Crear usuario admin por defecto si no existe
def create_admin_user():
    from models.usuario_model import Usuario
    from werkzeug.security import generate_password_hash
    
    admin_user = Usuario.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = Usuario(
            username='admin',
            email='admin@clinica.com',
            password=generate_password_hash('admin123'),
            rol='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Usuario admin creado: admin / admin123")
# AÑADE ESTO AL FINAL de tu run.py ACTUAL, justo antes de if __name__ == "__main__":

@app.route('/repair-db')
def repair_database():
    """Reparar base de datos manualmente."""
    try:
        from werkzeug.security import generate_password_hash
        from models.usuario_model import Usuario
        
        # Crear tablas
        db.create_all()
        
        # Crear usuario admin si no existe
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            admin = Usuario(
                username='admin',
                email='admin@clinica.com',
                password=generate_password_hash('admin123'),
                rol='admin',
                activo=True
            )
            db.session.add(admin)
            db.session.commit()
        
        return '''
        <h1>✅ Base de datos reparada</h1>
        <p>Usuario: <strong>admin</strong></p>
        <p>Contraseña: <strong>admin123</strong></p>
        <p><a href="/ingresar">Ir al login</a></p>
        '''
    except Exception as e:
        return f'<h1>❌ Error:</h1><pre>{str(e)}</pre>'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin_user()
      
    app.run(debug=True)
