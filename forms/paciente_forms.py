from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Optional

class PacienteForm(FlaskForm):
    dni = StringField('DNI', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    genero = SelectField('Género', choices=[('masculino', 'Masculino'), ('femenino', 'Femenino')], validators=[DataRequired()])
    telefono = StringField('Teléfono')
    email = StringField('Email', validators=[Optional(), Email()])
    direccion = StringField('Dirección')
    alergias = TextAreaField('Alergias')
    enfermedades_cronicas = TextAreaField('Enfermedades Crónicas')
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')