from database import db

class Servicio(db.Model):
    __tablename__ = 'servicios'
    
    id = db.Column(db.Integer, primary_key=True)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'))
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False, default=0.0)
    duracion_estimada = db.Column(db.Integer)
    activo = db.Column(db.Boolean, default=True)
    
    factura_detalles = db.relationship('FacturaDetalle', backref='servicio')
    
    def __repr__(self):
        return f'<Servicio {self.nombre}>'