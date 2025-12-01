from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import DataRequired

class CitaForm(FlaskForm):
    paciente_id = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    medico_id = SelectField('Médico', coerce=int, validators=[DataRequired()])
    fecha_cita = DateTimeField('Fecha y Hora', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    duracion = IntegerField('Duración (minutos)', default=30)
    tipo_consulta = SelectField('Tipo de Consulta', choices=[
        ('primera_vez', 'Primera Vez'),
        ('control', 'Control'),
        ('emergencia', 'Emergencia')
    ], validators=[DataRequired()])
    notas = TextAreaField('Notas')
    submit = SubmitField('Guardar')