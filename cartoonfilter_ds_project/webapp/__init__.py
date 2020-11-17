import os 

from flask import Flask, request, render_template, flash, redirect, url_for 
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from skimage import io as stikIO

from webapp.config import PATH_TO_DOWNLOADS
from webapp.forms import FileForm, LoginForm, RegistrationForm
from webapp.model import db, User
from webapp.utilits import security_checking, cartoonf_photo, photo_saver


Random_name = ''

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login' 
    
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    def allowed_file(filename):
        # Проверяет есть ли  расширение файла в списке разрешенных расширений
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg'}
    

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('greeting'))
        title = "Обработчик фотографий"
        file_form = FileForm()
        
        if security_checking():
            file = security_checking()
            if file_form.validate_on_submit(): # если не возникло ошибок при заполнении формы
            #считываем картинку сразу конвентируя информацию в ndarray
                file_in_ndarray = stikIO.imread(file)
                global Random_name
                if file_form.processing.data == 'cartoon_filter': # обработка фильтрамi
                    photo = cartoonf_photo(file_in_ndarray)
                
                elif file_form.processing.data == 'neural_network': # обработка ИИ
                    photo = neurof_photo(file_in_ndarray)
                Random_name = photo_saver(photo)  
                    
                return redirect(url_for('photo_processing'))                           
        # Список фото для карусели
        name_photo_example = ['liuyifei4.jpg', 'mountain4.jpg', 'photo1_cartoon.jpg',
                              'photo2_cartoon.jpg']
        path_photo_example = [os.path.join('static', 'images', name) for name in name_photo_example]
        return render_template('index.html', title=title, form=file_form, 
                                path_photo_example=path_photo_example)
    

    
    @app.route('/greeting')
    def greeting():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Приветствую!'

        return render_template('greeting.html', title=title)
    
    
    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', title=title, form=login_form)


    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('index'))
            
        flash('Имя пользователя или пароль неверны')
        return redirect(url_for('login'))        


    @app.route('/logout')
    def logout():
            logout_user()
            return redirect(url_for('index'))

    @app.route('/photo')
    def photo_processing():
        title = "Вот такое фото получилось"
        path_photo = os.path.join('static', 'images', 'downloads', Random_name)
        return render_template('photo.html', title=title, path_photo=path_photo)

    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        title = 'Регистрация'
        return render_template('registration.html', title=title, form=form)

    @app.route('/process-reg', methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            news_user = User(username=form.username.data, email=form.email.data, role='user')
            news_user.set_password(form.password.data)
            db.session.add(news_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('login'))
        flash('Пожалуйта исправьте ошибки в форме')
        return redirect(url_for('register'))

    return app
