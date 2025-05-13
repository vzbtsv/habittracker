from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email обязателен"),
        Email(message="Некорректный email")
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Пароль обязателен")
    ])
    remember_me = BooleanField('Запомнить меня')
