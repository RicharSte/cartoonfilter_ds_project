from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, RadioField


class FileForm(FlaskForm):
    photo = FileField('Картинка', validators=[FileRequired()], render_kw={"class": "form-group"})
    processing = RadioField('Выбор обработки фото', 
        choices=[('cartoon_filter','Обработка фильтрами'), 
            ('neural_network','Обработка искусственным интеллектом')])
    submit = SubmitField("Обработка", render_kw={"class": "btn btn-primary"})
    