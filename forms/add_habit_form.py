from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import CheckboxInput, ListWidget


class AddHabitForm(FlaskForm):
    name = StringField('Название привычки', validators=[DataRequired(message="Это поле обязательно")])
    description = TextAreaField('Описание')
    days_of_week = SelectMultipleField('Дни недели', choices=[
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье')
    ])
    submit = SubmitField('Добавить привычку')
