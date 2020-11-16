import os
from random import randint

from flask import request, redirect, flash, url_for 
from werkzeug.utils import secure_filename
from PIL import Image

from filters import cartoonise_using_cartoonfilter 
from neuro_filters import cartoonize_using_network_without_filters
from webapp.config import PATH_TO_DOWNLOADS

def allowed_file(filename):
        # Проверяет есть ли  расширение файла в списке разрешенных расширений
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg'}
    
def security_checking():
    if request.method == 'POST':
        # Проверка есть ли файл в запросе
        if 'photo' not in request.files:
            flash('Нет файла')
            return redirect(request.url)
        file = request.files['photo']
        print(file, 1)
        # Если пользователь не выбирает файл, 
        # браузер может отправить пустую часть без имени файла
        if file.filename == '':
            flash("Файл не выбран")
            return redirect(request.url)
        # Если расширение файла в списке разрешенных
        if file and allowed_file(file.filename):
            # проверка безопасности имени файла
            filename = secure_filename(file.filename)
            return file
        flash("Я не могу принять этот файл")
        return redirect(request.url)

def photo_saver(photo):
    photo = Image.open(photo)
    #даем случайное имя файлу, чтобы отправить его пользовате    
    random_name = str(randint(0, 10000))+'.jpeg'
    #скачиваем фотo
    photo.save(os.path.join(PATH_TO_DOWNLOADS, random_name))
    return random_name 

def cartoonf_photo(file_in_ndarray):
    try:
        photo = cartoonise_using_cartoonfilter(file_in_ndarray) 
        return photo         
    except TypeError:
        # Если невозможно обработать фото, то пользователь видит
        flash('это фото невозможно обработать, выберите другое')
        return redirect(url_for('index'))
    return redirect(url_for('photo_processing'))

def neurof_photo(file_in_ndarray):
    #обрабатываем фото, на выходе данные находятся в формате _io.BytesIO
    photo = cartoonize_using_network_without_filters(file_in_ndarray)
    return photo
