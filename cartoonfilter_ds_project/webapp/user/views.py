from flask import Blueprint, flash, render_template, redirect, url_for 
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import db, User


blueprint = Blueprint('user', __name__, url_prefix='/user')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('photo.index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('login.html', title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('photo.index'))
        
    flash('Имя пользователя или пароль неверны')
    return redirect(url_for('user.login'))        


@blueprint.route('/logout')
def logout():
        logout_user()
        return redirect(url_for('photo.index'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('photo.index'))
    form = RegistrationForm()
    title = 'Регистрация'
    return render_template('registration.html', title=title, form=form)

@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        news_user = User(username=form.username.data, email=form.email.data, role='user')
        news_user.set_password(form.password.data)
        db.session.add(news_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались')
        return redirect(url_for('user.login'))
    flash('Пожалуйта исправьте ошибки в форме')
    return redirect(url_for('user.register'))