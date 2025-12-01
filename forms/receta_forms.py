from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class RecetaForm(FlaskForm):
    consulta_id = SelectField('Consulta', coerce=int, validators=[DataRequired()])
    medicamento = StringField('Medicamento', validators=[DataRequired()])
    dosis = StringField('Dosis')
    frecuencia = StringField('Frecuencia')
    duracion = StringField('Duración')
    instrucciones = TextAreaField('Instrucciones')
    submit = SubmitField('Guardar')