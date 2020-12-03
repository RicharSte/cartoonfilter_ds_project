import os 

from flask import Flask, render_template, redirect, session, url_for 
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

from webapp.config import PHOTO_PATH, PHOTO_PATH_CAROUSEL, NAME_PHOTO_EXAMPLE
from webapp.photo.views import blueprint as photo_blueprint
from webapp.user.models import db, User
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(photo_blueprint)
    
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
 

    #главная страница
    @app.route('/')
    def greeting():
        if current_user.is_authenticated:
            return redirect(url_for('photo.index'))
        title = 'Приветствую!'

        path_photo_example = [os.path.join(PHOTO_PATH_CAROUSEL, name) for name in NAME_PHOTO_EXAMPLE]

        return render_template('greeting.html', title=title, path_photo_example=path_photo_example)

    @app.route('/result')
    def photo_processing():
        title = "Вот такое фото получилось"
        random_name = session.get('random_name', None)
        path_photo = os.path.join(PHOTO_PATH, random_name)
        return render_template('photo.html', title=title, path_photo=path_photo)
  
    return app
