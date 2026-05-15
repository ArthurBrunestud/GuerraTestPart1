from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    dni      = StringField('DNI', validators=[DataRequired(), Length(min=8, max=8)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit   = SubmitField('Ingresar')