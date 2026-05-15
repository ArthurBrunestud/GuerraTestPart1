from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class MovimientoForm(FlaskForm):
    producto_id  = SelectField('Producto', coerce=int, validators=[DataRequired()])
    proveedor_id = SelectField('Proveedor', coerce=int, validators=[Optional()])
    tipo         = SelectField('Tipo', choices=[('entrada', 'Entrada'), ('salida', 'Salida')],
                               validators=[DataRequired()])
    cantidad     = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1, max=100000)])
    notas        = TextAreaField('Notas', validators=[Optional()])
    submit       = SubmitField('Registrar')