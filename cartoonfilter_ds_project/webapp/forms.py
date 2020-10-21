from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    photo = FileField('Картинка', validators=[FileRequired()], render_kw={"class": "form-group"})
    processing = RadioField('Что-то', choices=[('cartoon_filter','Обработка фильтрами'),
                                              ('neural_network','Обработка искусственным интеллектом')])
    submit = SubmitField("Обработка", render_kw={"class": "btn btn-primary"})

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class':"form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class':"form-control"})
    submit = SubmitField('Отправить', render_kw={'class':"btn btn-primary"})