from database import db

class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    fecha_consulta = db.Column(db.DateTime, nullable=False)
    sintomas = db.Column(db.Text)
    diagnostico = db.Column(db.Text)
    tratamiento = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    peso = db.Column(db.Float)
    altura = db.Column(db.Float)
    presion_arterial = db.Column(db.String(20))
    temperatura = db.Column(db.Float)
    costo = db.Column(db.Float, nullable=False, default=0.0)
    
    recetas = db.relationship('Receta', backref='consulta')
    factura_detalles = db.relationship('FacturaDetalle', backref='consulta')
    
    def __repr__(self):
        return f'<Consulta {self.id} - {self.paciente.nombre}>'