from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///saludplus.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clave-secreta-muy-segura-aqui"

# Inicializar la base de datos
db = SQLAlchemy(app)

# FORZAR IMPORTACIÓN DE TODOS LOS MODELOS PRIMERO
# Importar explícitamente cada modelo para que SQLAlchemy los registre
from models.usuario_model import Usuario
from models.medico_model import Medico
from models.paciente_model import Paciente
from models.especialidad_model import Especialidad
from models.cita_model import Cita
from models.consulta_model import Consulta
from models.receta_model import Receta
from models.servicio_model import Servicio
from models.factura_model import Factura
from models.factura_detalle_model import FacturaDetalle
from models.horario_medico_model import HorarioMedico
from models.configuracion_model import Configuracion

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# FUNCIÓN PARA INICIALIZAR BASE DE DATOS
def init_database():
    """Inicializa la base de datos y crea el usuario admin."""
    try:
        # PASO 1: Crear todas las tablas
        db.create_all()
        print("✓ Tablas de base de datos creadas")
        
        # IMPORTANTE: Hacer commit explícito para SQLite
        db.session.commit()
        
        # PASO 2: Crear usuario admin por defecto si no existe
        from werkzeug.security import generate_password_hash
        
        # Esperar un momento para asegurar que las tablas estén listas
        import time
        time.sleep(0.5)
        
        # Usar db.session.execute para verificar si la tabla existe
        try:
            # Intentar consultar si la tabla existe
            result = db.session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
            table_exists = result.fetchone() is not None
            
            if not table_exists:
                print("⚠️ La tabla 'usuarios' no existe, recreando...")
                db.create_all()
                db.session.commit()
        except:
            pass
        
        # Ahora intentar crear el usuario admin
        admin_user = Usuario.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = Usuario(
                username='admin',
                email='admin@clinica.com',
                password=generate_password_hash('admin123'),
                rol='admin',
                activo=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Usuario admin creado: admin / admin123")
        else:
            print("ℹ️ Usuario admin ya existe")
            
    except Exception as e:
        print(f"⚠️ Error al inicializar base de datos: {e}")
        # Intentar una segunda vez
        try:
            db.session.rollback()
            db.create_all()
            db.session.commit()
            print("✓ Tablas recreadas en segundo intento")
        except Exception as e2:
            print(f"⚠️ Error en segundo intento: {e2}")

# Inicializar base de datos al iniciar
with app.app_context():
    init_database()

# Importar y registrar blueprints
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

@app.route('/index')
def index():
    return redirect(url_for('welcome.index'))

if __name__ == "__main__":
    app.run(debug=True)