# forms/factura_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, DecimalField, SelectField
from wtforms.validators import DataRequired, Optional

class FacturaForm(FlaskForm):
    paciente_id = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    numero_factura = StringField('Número de Factura', validators=[DataRequired()])
    fecha_emision = DateTimeField('Fecha Emisión', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    estado = SelectField('Estado', choices=[
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'), 
        ('cancelada', 'Cancelada')
    ], validators=[DataRequired()])
    subtotal = DecimalField('Subtotal', validators=[DataRequired()])
    impuesto = DecimalField('Impuesto', validators=[DataRequired()])
    total = DecimalField('Total', validators=[DataRequired()])
    metodo_pago = SelectField('Método de Pago', choices=[
        ('', 'Seleccionar método...'),
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia')
    ], validators=[Optional()])