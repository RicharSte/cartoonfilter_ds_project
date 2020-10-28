from pathlib import Path

from flask import Flask, request, render_template, flash, redirect, url_for 
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from PIL import Image
from skimage import io as stikIO
from werkzeug.utils import secure_filename 

from cartoonise_using_cartoonfilter import cartoonise_using_cartoonfilter
from cartoonize_using_network_without_filters import cartoonize_using_network_without_filters
from webapp.forms import FileForm, LoginForm
from webapp.model import db, User

PATH_TO_DOWNLOADS = Path('downloads/photo.jpeg')

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
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
            flash('Ок')
            #считываем картинку сразу конвентируя информацию в ndarray
            file_in_ndarray = stikIO.imread(file)

            if file_form.processing.data == 'cartoon_filter': # обработка фильтрами
                flash('Обработка фильтрами')
                try:
                    photo = cartoonise_using_cartoonfilter(file_in_ndarray) 
                    photo = Image.open(photo)
                #скачиваем фото
                    photo.save(PATH_TO_DOWNLOADS)          
                except TypeError:
                    #АХТУНГ это наддо выводить на экран пользователю, если не возможно обработать фото
                    print('это фото невозможно обработать, выберите другое')
                return redirect(url_for('photo_processing'))
            
            elif file_form.processing.data == 'neural_network': # обработка ИИ
                flash('Обработка ИИ')
            #обрабатываем фото, на выходе данные находятся в формате _io.BytesIO
                photo = cartoonize_using_network_without_filters(file_in_ndarray)
                photo = Image.open(photo)
            #скачиваем фото
                photo.save(PATH_TO_DOWNLOAD)         
            return redirect(url_for('photo_processing'))
        return render_template('index.html', title=title, form=file_form)
    
    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Аторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)
     
    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            
        flash('Username or password are not correct')
        return redirect(url_for('login'))        

    @app.route('/logout')
    def logout():
            logout_user()
            return redirect(url_for('index'))
    
    @app.route('/photo')
    def photo_processing():
        title = "Вот такое фото получилось"
        return render_template('photo.html', title=title)

#идея в том чтобы для не зарегистрированных пользователей не была доступна возможность 
#отбрабатывать фотки на сайте. Т.е. нужно дописать Главную страницу, которая будет показываться всем
#а после регистрации была страница с обработчиком фото (это можно передать наташе, пока я займусь S3)     
    @login_required
    def func():
        pass
    
    
    return app

