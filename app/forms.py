from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class PuzzleForm(FlaskForm):
    letters = StringField("Letters", validators=[DataRequired()])