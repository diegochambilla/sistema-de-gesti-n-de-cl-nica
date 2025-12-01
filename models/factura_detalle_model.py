from database import db

class FacturaDetalle(db.Model):
    __tablename__ = 'factura_detalles'
    
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id'))
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'))
    descripcion = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Float, nullable=False, default=0.0)
    subtotal = db.Column(db.Float, nullable=False, default=0.0)
    
    def __repr__(self):
        return f'<FacturaDetalle {self.descripcion}>'