from database import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    direccion = db.Column(db.String(200))
    alergias = db.Column(db.Text)
    enfermedades_cronicas = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, default=db.func.now())
    activo = db.Column(db.Boolean, default=True)
    
    citas = db.relationship('Cita', backref='paciente')
    consultas = db.relationship('Consulta', backref='paciente')
    facturas = db.relationship('Factura', backref='paciente')
    
    def __repr__(self):
        return f'<Paciente {self.nombre} {self.apellido}>'