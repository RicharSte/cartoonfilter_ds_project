import os 

from flask import Blueprint, flash, render_template, redirect, session, url_for 
from flask_login import current_user
from skimage import io as stikIO

from webapp.config import PHOTO_PATH
from webapp.photo.forms import FileForm
from webapp.s3_photo_upload import download_photo_s3
from webapp.utilits import security_checking, cartoonf_photo, neurof_photo, photo_saver
from webapp.utilits import security_checking, cartoonf_photo, photo_saver


blueprint = Blueprint('photo', __name__, url_prefix='/photo')

@blueprint.route('/', methods=['GET', 'POST'])
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

            if file_form.processing.data == 'cartoon_filter': # обработка фильтрами
                photo = cartoonf_photo(file_in_ndarray)
            elif file_form.processing.data == 'neural_network': # обработка ИИ
                    photo = neurof_photo(file_in_ndarray)
            random_name = photo_saver(photo)
            # берём айди пользователя, чтобы сделать для него папку на амазоне
            User_id = str(current_user)[1:-1] 
            # используем амазон, чтобы сохранить исходник фото
            download_photo_s3(file_in_ndarray, User_id, random_name)
            session['random_name'] = random_name
                
            return redirect(url_for('photo_processing'))         
        flash('Пожалуйта, повторите выбор файла и выберите способ обработки')
        return redirect(url_for('photo.index'))

    return render_template('index.html', title=title, form=file_form)


