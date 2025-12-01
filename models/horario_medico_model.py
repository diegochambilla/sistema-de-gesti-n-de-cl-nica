from database import db

class HorarioMedico(db.Model):
    __tablename__ = 'horarios_medicos'
    
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<HorarioMedico {self.medico.usuario.username} - {self.dia_semana}>'