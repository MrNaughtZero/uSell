from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, FileField, TextAreaField, DecimalField
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email('Please enter a valid email'), Length(max=300)])
    password = PasswordField(validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=8), EqualTo('password', message='Oops! Your Passwords do not match')])

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email('Please enter a valid email'), Length(max=300)])
    password = PasswordField(validators=[InputRequired(), Length(min=8)])

class ProductForm(FlaskForm):
    store_name = StringField('Store Name', validators=[InputRequired()])
    item_name = StringField('Item Name', validators=[InputRequired()])
    item_desc = TextAreaField('Item Description', validators=[InputRequired(), Length(max=500)])
    item_currency = SelectField('Currency', validators=[InputRequired()], choices=[('gbp', '£'), ('usd', '$')])
    item_price = DecimalField('Price', validators=[InputRequired()], widget=h5widgets.NumberInput(min=1, step=1))
    item_img = FileField('Item Image', validators=[InputRequired()])
    contact_email = StringField('Contact Email', validators=[InputRequired(), Email('Please enter a valid email')])

class StoreUrl(FlaskForm):
    store_url = StringField('Store URL', validators=[InputRequired(), Length(max=100)])