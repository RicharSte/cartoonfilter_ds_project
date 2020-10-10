from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FileForm(FlaskForm):
    photo = FileField('картинка', validators=[FileRequired()],
                      FileAllowed(['jpg', 'png'], 'Только фотографии!'), render_kw={"class": "form-file-input"})
    cortoon_filter = SubmitField("Обработка фильтрами", render_kw={"class": "btn btn-primary"})
    neural_network = SubmitField("Обработка искусственным интеллектом", 
                                render_kw={"class": "btn btn-primary"})
    # urrent_app.config['UPLOAD_FOLDER']
