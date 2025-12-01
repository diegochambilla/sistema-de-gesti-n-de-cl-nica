from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

class UsuarioForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[Optional(), Length(min=6)])
    rol = SelectField('Rol', choices=[
        ('usuario', 'Usuario'), 
        ('medico', 'Médico'), 
        ('recepcion', 'Recepcionista'), 
        ('admin', 'Administrador')
    ])
    activo = BooleanField('Activo')
    submit = SubmitField('Guardar')