from flask import Flask, render_template

from webapp.forms import FileForm

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.route('/')
    def index():
        title = "Обработчик фотографий"
        file_form = FileForm()
        if file_form.validate_on_submit():
            file_form.photo.data
            filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(app.instance_path, 'photos', filename))
        return render_template('index.html', title=title, form=file_form)

    return app

