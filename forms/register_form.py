from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[
        DataRequired(message="Имя обязательно"),
        Length(min=2, max=50)
    ])

    email = StringField('Email', validators=[
        DataRequired(message="Email обязателен"),
        Email(message="Некорректный email"),
        Length(max=120)
    ])

    password = PasswordField('Пароль', validators=[
        DataRequired(message="Пароль обязателен"),
    ])

    password_confirm = PasswordField('Подтвердите пароль', validators=[
        DataRequired(message="Подтверждение пароля обязательно"),
        EqualTo('password', message="Пароли должны совпадать")
    ])

    submit = SubmitField('Зарегистрироваться')
