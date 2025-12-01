from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired

class MedicoForm(FlaskForm):
    usuario_id = SelectField('Usuario', coerce=int, validators=[DataRequired()])
    especialidad_id = SelectField('Especialidad', coerce=int, validators=[DataRequired()])
    numero_colegiado = StringField('Número de Colegiado', validators=[DataRequired()])
    telefono = StringField('Teléfono')
    direccion = StringField('Dirección')
    fecha_contratacion = DateField('Fecha de Contratación', validators=[DataRequired()])
    activo = BooleanField('Activo')
    submit = SubmitField('Guardar')

class HorarioMedicoForm(FlaskForm):
    dia_semana = SelectField('Día de la semana', choices=[
        (1, 'Lunes'), (2, 'Martes'), (3, 'Miércoles'), 
        (4, 'Jueves'), (5, 'Viernes'), (6, 'Sábado'), (7, 'Domingo')
    ], coerce=int, validators=[DataRequired()])
    hora_inicio = StringField('Hora inicio (HH:MM)', validators=[DataRequired()])
    hora_fin = StringField('Hora fin (HH:MM)', validators=[DataRequired()])
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')