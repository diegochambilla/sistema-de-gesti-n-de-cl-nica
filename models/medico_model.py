from database import db

class Medico(db.Model):
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    numero_colegiado = db.Column(db.String(50), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    fecha_contratacion = db.Column(db.Date, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    citas = db.relationship('Cita', backref='medico')
    consultas = db.relationship('Consulta', backref='medico')
    horarios = db.relationship('HorarioMedico', backref='medico')
    
    def __repr__(self):
        return f'<Medico {self.usuario.username}>'