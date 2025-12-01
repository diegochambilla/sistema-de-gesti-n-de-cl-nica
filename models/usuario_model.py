from database import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='usuario')
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    
    medico = db.relationship('Medico', backref='usuario', uselist=False)
    
    def __repr__(self):
        return f'<Usuario {self.username}>'
    
    def get_id(self):
        return str(self.id)