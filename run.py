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

# PRIMERO Y MÁS IMPORTANTE: Importar TODOS los modelos ANTES de cualquier otra cosa
# Esto asegura que SQLAlchemy registre los modelos
import models  # <-- ESTA LÍNEA ES CLAVE
from models import Usuario  # <-- Importa Usuario para el login_manager

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

# Configurar el loader de usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# SEGUNDO: Crear tablas y usuario admin
def init_database():
    """Inicializa la base de datos y crea el usuario admin."""
    try:
        # IMPORTANTE: Forzar que SQLAlchemy vea todos los modelos
        # Esto asegura que todos los modelos estén registrados
        from models import (
            Usuario, Medico, Paciente, Especialidad, Cita, 
            Consulta, Receta, Servicio, Factura, FacturaDetalle,
            HorarioMedico, Configuracion
        )
        
        # Crear todas las tablas
        db.create_all()
        print("✓ Tablas de base de datos creadas")
        
        # Crear usuario admin por defecto si no existe
        from werkzeug.security import generate_password_hash
        
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
            print("ℹ️ Puedes cambiar la contraseña después de iniciar sesión")
        else:
            print("ℹ️ Usuario admin ya existe")
            
        # Verificar que las tablas se crearon
        print(f"ℹ️ Número de tablas creadas: {len(db.metadata.tables)}")
            
    except Exception as e:
        print(f"⚠️ Error al inicializar base de datos: {e}")
        import traceback
        traceback.print_exc()

# Inicializar base de datos al iniciar
with app.app_context():
    init_database()

# TERCERO: Importar y registrar blueprints
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