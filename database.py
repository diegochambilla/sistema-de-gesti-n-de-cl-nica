from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Configuración para evitar problemas de compatibilidad
def init_app(app):
    db.init_app(app)
    return db