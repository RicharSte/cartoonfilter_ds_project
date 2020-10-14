from flask import Flask, render_template, flash, redirect, url_for

from webapp.forms import FileForm

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.route('/', methods=['POST', 'GET'])
    def index():
        title = "Обработчик фотографий"
        file_form = FileForm()
        if file_form.validate_on_submit(): # если не возникло ошибок при заполнении формы
            flash('Ок')
            #file_form.photo.data
            # Защита имени файла
            filename = secure_filename(photo_file.filename)
            # Сохранение фото
            photo.save(os.path.join(app.instance_path, 'photos', filename))

            if request.file_form['processing'] == 'cortoon_filter': # обработка фильтрами
                flash('Обработка фильтрами')
                return redirect(url_for('photo_processing'))
            elif request.file_form['processing'] == 'neural_network': # обработка ИИ
                flash('Обработка ИИ')
        return render_template('index.html', title=title, form=file_form)

    


    @app.route('/photo')
    def photo_processing():
        title = "Вот такое фото получилось"
        return render_template('photo.html', title=title)

    return app

