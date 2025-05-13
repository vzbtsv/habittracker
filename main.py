from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.db_session import global_init, create_session
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.add_habit_form import AddHabitForm
import os
from data.user import User
from data.habit import Habit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceumsecretkey'

db_path = os.path.join(os.path.dirname(__file__), 'db', 'habits.db')
global_init(db_path)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    from data.user import User
    session = create_session()
    user = session.query(User).get(int(user_id))
    session.close()
    return user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('habits'))
        flash('Неверный email или пароль', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('habits'))

    form = RegisterForm()
    if form.validate_on_submit():
        session = create_session()

        if session.query(User).filter(User.email == form.email.data).first():
            flash('Пользователь с таким email уже зарегистрирован', 'danger')
            session.close()
            return redirect(url_for('register'))

        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        try:
            session.add(user)
            session.commit()
            flash('Регистрация прошла успешно.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            session.rollback()
            flash('Ошибка при регистрации: ' + str(e), 'danger')
        finally:
            session.close()

    return render_template('register.html', title='Register', form=form)


@app.route('/habits')
@login_required
def habits():
    session = create_session()
    habits = session.query(Habit).filter(Habit.user_id == current_user.id).all()

    for habit in habits:
        days_of_week_list = habit.days_of_week.split(',')
        days_of_week_str = ', '.join([
            'Пн' if day == '0' else 'Вт' if day == '1' else 'Ср' if day == '2' else 'Чт' if day == '3' else 'Пт' if day == '4' else 'Сб' if day == '5' else 'Вс'
            for day in days_of_week_list])
        habit.days_of_week = days_of_week_str

    return render_template('habits.html', habits=habits)


@app.route('/add_habit', methods=['GET', 'POST'])
@login_required
def add_habit():
    form = AddHabitForm()
    if form.validate_on_submit():
        session = create_session()
        selected_days = form.days_of_week.data
        days_of_week_str = ','.join(map(str, selected_days))

        habit = Habit(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id,
            days_of_week=days_of_week_str
        )
        session.add(habit)
        session.commit()
        flash('Привычка успешно добавлена!', 'success')
        return redirect(url_for('habits'))

    return render_template('add_habit.html', form=form)


@app.route('/delete_habit/<int:habit_id>', methods=['POST'])
@login_required
def delete_habit(habit_id):
    session = create_session()
    habit = session.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if habit:
        session.delete(habit)
        session.commit()
        flash('Привычка удалена.', 'success')
    else:
        flash('Ошибка. Привычка не удалена.', 'danger')
    session.close()
    return redirect(url_for('habits'))


if __name__ == '__main__':
    app.run()
