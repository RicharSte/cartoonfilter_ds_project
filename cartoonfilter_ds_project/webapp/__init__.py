import os

from flask import Flask, request, render_template, flash, redirect, url_for
from PIL import Image
from skimage import io as stikIO
from werkzeug.utils import secure_filename

from cartoonise_using_cartoonfilter import cartoonise_using_cartoonfilter
from cartoonize_using_network_without_filters import cartoonize_using_network_without_filters
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

        if file_form.validate_on_submit(): # если не возникло ошибок при заполнении формы
            flash('Ок')
            #считываем картинку сразу конвентируя информацию в ndarray
            file_in_ndarray = stikIO.imread(file)

            if file_form.processing.data == 'cartoon_filter': # обработка фильтрами
                flash('Обработка фильтрами')
                try:
                    photo = cartoonise_using_cartoonfilter(file_in_ndarray) 
                    photo = Image.open(photo)
                #скачиваем фото
                    photo.save('webapp/static/images/downloads/photo.jpeg')          
                except TypeError:
                    #АХТУНГ это наддо выводить на экран пользователю, если не возможно обработать фото
                    flash('это фото невозможно обработать, выберите другое')
                return redirect(url_for('photo_processing'))
            
            elif file_form.processing.data == 'neural_network': # обработка ИИ
                flash('Обработка ИИ')
            #обрабатываем фото, на выходе данные находятся в формате _io.BytesIO
                photo = cartoonize_using_network_without_filters(file_in_ndarray)
                photo = Image.open(photo)
            #скачиваем фото
                photo.save('webapp/static/images/downloads/photo.jpeg')
            return redirect(url_for('photo_processing'))
        return render_template('index.html', title=title, form=file_form)
    

    @app.route('/photo')
    def photo_processing():
        title = "Вот такое фото получилось"
        return render_template('photo.html', title=title)

    return app

