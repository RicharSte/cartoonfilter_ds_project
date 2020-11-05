import os
from random import randint

from flask import Flask, request, render_template, flash, redirect, url_for 
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from PIL import Image
from skimage import io as stikIO
from werkzeug.utils import secure_filename 

from filters import cartoonise_using_cartoonfilter
from filters import cartoonize_using_network_without_filters
from webapp.forms import FileForm, LoginForm, RegistrationForm
from webapp.model import db, User

PATH_TO_DOWNLOADS = os.path.join(
os.path.abspath(os.path.dirname(__file__)), 'static', 'images', 'downloads')

RANDOM_NAME = ''

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
                #считываем картинку сразу конвентируя информацию в ndarray
                    file_in_ndarray = stikIO.imread(file)

                    if file_form.processing.data == 'cartoon_filter': # обработка фильтрами
                        flash('Обработка фильтрами')
                        try:
                            photo = cartoonise_using_cartoonfilter(file_in_ndarray) 
                            photo = Image.open(photo)
                        #даем случайное имя файлу, чтобы отправить его пользовате    
                            random_name = str(randint(0, 10000))+'.jpeg'
                            global RANDOM_NAME
                            RANDOM_NAME = random_name
                        #скачиваем фотo
                            photo.save(os.path.join(PATH_TO_DOWNLOADS, RANDOM_NAME))         
                        
                        except TypeError:
                            # Если невозможно обработать фото, то пользователь видит
                            flash('это фото невозможно обработать, выберите другое')
                            return redirect(url_for('index'))
                        return redirect(url_for('photo_processing'))
                    
                    elif file_form.processing.data == 'neural_network': # обработка ИИ
                        flash('Обработка ИИ')
                    #обрабатываем фото, на выходе данные находятся в формате _io.BytesIO
                        photo = cartoonize_using_network_without_filters(file_in_ndarray)
                        photo = Image.open(photo)
                    #даем случайное имя файлу, чтобы отправить его пользователю
                        random_name = str(randint(0, 10000))+'.jpeg'
                        RANDOM_NAME = random_name
                    #сохраняем файл
                        photo.save(os.path.join(PATH_TO_DOWNLOADS, RANDOM_NAME))         
                    return redirect(url_for('photo_processing'))
          
        name_photo_example = ['liuyifei4.jpg', 'mountain4.jpg', 'photo1_cartoon.jpg',
                              'photo2_cartoon.jpg']
        path_photo_example = [os.path.join('static', 'images', name) for name in name_photo_example]
        return render_template('index.html', title=title, form=file_form, 
                                path_photo_example=path_photo_example)
    

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
        path_photo = os.path.join('static', 'images', 'downloads', RANDOM_NAME)
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
