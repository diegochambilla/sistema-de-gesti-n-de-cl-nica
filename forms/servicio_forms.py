from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired

class ServicioForm(FlaskForm):
    especialidad_id = SelectField('Especialidad', coerce=int)
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    precio = FloatField('Precio', validators=[DataRequired()])
    duracion_estimada = IntegerField('Duración Estimada (minutos)')
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')