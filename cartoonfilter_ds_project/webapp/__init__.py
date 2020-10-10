from flask import (Flask, render_template)

from webapp.forms import FileForm

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.route('/')
    def index():
        title = "Обработчик фотографий"
        file_form = FileForm()
        if form.validate_on_submit():
            form.photo.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.instance_path, 'photos', filename))
        return render_template('index.html', title=title, form=file_form)

    return app

