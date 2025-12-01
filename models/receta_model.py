from database import db

class Receta(db.Model):
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=False)
    medicamento = db.Column(db.String(200), nullable=False)
    dosis = db.Column(db.String(100))
    frecuencia = db.Column(db.String(100))
    duracion = db.Column(db.String(100))
    instrucciones = db.Column(db.Text)
    fecha_prescripcion = db.Column(db.DateTime, default=db.func.now())
    
    def __repr__(self):
        return f'<Receta {self.medicamento}>'