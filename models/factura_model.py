from database import db

class Factura(db.Model):
    __tablename__ = 'facturas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    numero_factura = db.Column(db.String(50), unique=True, nullable=False)
    fecha_emision = db.Column(db.DateTime, default=db.func.now())
    subtotal = db.Column(db.Float, nullable=False, default=0.0)
    impuesto = db.Column(db.Float, nullable=False, default=0.0)
    total = db.Column(db.Float, nullable=False, default=0.0)
    estado = db.Column(db.String(20), default='pendiente')
    metodo_pago = db.Column(db.String(50))
    fecha_pago = db.Column(db.DateTime)
    
    detalles = db.relationship('FacturaDetalle', backref='factura')
    
    def __repr__(self):
        return f'<Factura {self.numero_factura}>'