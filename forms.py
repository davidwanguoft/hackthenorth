from flask_wtf import Form
from wtforms import StringField, IntegerField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired,Length, ValidationError, NumberRange, EqualTo

