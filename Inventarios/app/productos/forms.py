from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProductoForm(FlaskForm):
    nombre        = StringField('Nombre', validators=[DataRequired(), Length(max=150)])
    descripcion   = TextAreaField('Descripción', validators=[Optional()])
    categoria     = SelectField('Categoría', choices=[
                        ('Ropa', 'Ropa'),
                        ('Electrodomésticos', 'Electrodomésticos'),
                        ('Otro', 'Otro')
                    ], validators=[DataRequired()])
    marca         = StringField('Marca', validators=[Optional(), Length(max=80)])
    precio_compra = DecimalField('Precio de compra', validators=[DataRequired(), NumberRange(min=0.01, max=999999.99)])
    moneda        = SelectField('Moneda', choices=[
                        ('PEN', 'PEN - Sol'),
                        ('USD', 'USD - Dólar'),
                    ], validators=[DataRequired()])
    stock         = IntegerField('Cantidad en stock', validators=[DataRequired(), NumberRange(min=0, max=100000)])
    imagen        = FileField('Imagen del producto', validators=[
                        Optional(),
                        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Solo imágenes.')
                    ])
    submit        = SubmitField('Guardar producto')


class DesactivarForm(FlaskForm):
    pass