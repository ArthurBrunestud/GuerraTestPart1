from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

class ProveedorForm(FlaskForm):
    nombre    = StringField('Nombre', validators=[DataRequired(), Length(max=150)])
    telefono  = StringField('Teléfono', validators=[
                    Optional(),
                    Regexp(r'^\d{9}$', message='El teléfono debe tener exactamente 9 dígitos numéricos.')
                ])
    direccion = TextAreaField('Dirección', validators=[Optional()])
    submit    = SubmitField('Guardar')

class EmptyForm(FlaskForm):
    pass