from database import db

class Cita(db.Model):
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    fecha_cita = db.Column(db.DateTime, nullable=False)
    duracion = db.Column(db.Integer, default=30)
    estado = db.Column(db.String(20), default='programada')
    tipo_consulta = db.Column(db.String(50))
    notas = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    
    consulta = db.relationship('Consulta', backref='cita', uselist=False)
    
    def __repr__(self):
        return f'<Cita {self.id} - {self.paciente.nombre}>'