from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, BooleanField
from wtforms.validators import DataRequired

class EspecialidadForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    precio_consulta = FloatField('Precio Consulta', validators=[DataRequired()])
    activa = BooleanField('Activa', default=True)
    submit = SubmitField('Guardar')