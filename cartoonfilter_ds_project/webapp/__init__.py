import os

from flask import Flask, request, render_template, flash, redirect, url_for
from io import StringIO
from werkzeug.utils import secure_filename

from webapp.forms import FileForm


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    def allowed_file(filename):
        # Проверяет есть ли  расширение файла в списке разрешенных расширений
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg'}

    @app.route('/', methods=['GET', 'POST'])
    def index():
        title = "Обработчик фотографий"
        file_form = FileForm()
        if request.method == 'POST':
            # Проверка есть ли файл в запросе
            if 'photo' not in request.files:
                flash('Нет файла')
                return redirect(request.url)
            file = request.files['photo']
            # Если пользователь не выбирает файл, 
            # браузер может отправить пустую часть без имени файла
            if file.filename == '':
                flash("Файл не выбран")
                return redirect(request.url)
            # Если расширение файла в списке разрешенных
            if file and allowed_file(file.filename):
                # проверка безопасности имени файла
                filename = secure_filename(file.filename)
                file_in_bytes = file.read()
                return file_in_bytes
                
                # Сохранение файла
                #file.save(os.path.abspath(os.path.join("downloads", filename)))

        if file_form.validate_on_submit(): # если не возникло ошибок при заполнении формы
            flash('Ок')

            if file_form.processing.data == 'cartoon_filter': # обработка фильтрами
                flash('Обработка фильтрами')
                return redirect(url_for('photo_processing'))
            elif file_form.processing.data == 'neural_network': # обработка ИИ
                flash('Обработка ИИ')
            return redirect(url_for('photo_processing'))
        return render_template('index.html', title=title, form=file_form)
    

    @app.route('/photo')
    def photo_processing():
        title = "Вот такое фото получилось"
        return render_template('photo.html', title=title)

    return app

