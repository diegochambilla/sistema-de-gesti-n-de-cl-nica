from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ConfiguracionForm(FlaskForm):
    clave = StringField('Clave', validators=[DataRequired()])
    valor = TextAreaField('Valor', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    submit = SubmitField('Guardar')