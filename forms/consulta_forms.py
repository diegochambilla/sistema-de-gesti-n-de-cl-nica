from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, DateTimeField, SelectField
from wtforms.validators import DataRequired

class ConsultaForm(FlaskForm):
    cita_id = SelectField('Cita', coerce=int, validators=[DataRequired()])
    fecha_consulta = DateTimeField('Fecha Consulta', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    sintomas = TextAreaField('Síntomas')
    diagnostico = TextAreaField('Diagnóstico')
    tratamiento = TextAreaField('Tratamiento')
    observaciones = TextAreaField('Observaciones')
    peso = FloatField('Peso (kg)')
    altura = FloatField('Altura (cm)')
    presion_arterial = StringField('Presión Arterial')
    temperatura = FloatField('Temperatura (°C)')
    costo = FloatField('Costo', validators=[DataRequired()])
    submit = SubmitField('Guardar')