from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FileForm(FlaskForm):
    photo = FileField('картинка', validators=[FileRequired()],
                      
                      render_kw={"class": "form-group"})
    submit = SubmitField("Обработка", 
                             render_kw={"class": "btn btn-primary"})

