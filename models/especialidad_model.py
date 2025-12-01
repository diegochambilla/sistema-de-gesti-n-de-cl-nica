from database import db

class Especialidad(db.Model):
    __tablename__ = 'especialidades'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    precio_consulta = db.Column(db.Float, nullable=False, default=0.0)
    activa = db.Column(db.Boolean, default=True)
    
    medicos = db.relationship('Medico', backref='especialidad')
    servicios = db.relationship('Servicio', backref='especialidad')
    
    def __repr__(self):
        return f'<Especialidad {self.nombre}>'