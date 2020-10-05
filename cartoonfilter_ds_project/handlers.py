import os
#я не знаю что из этого нужно в этом модуле, а что нет, поэтому беру все
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import ReplyKeyboardMarkup, utils
import cartoonize
import requests
import shutil

import numpy as np
import cv2
from PIL import Image
import io

from cartoon_filter import apply_cartoon_filter

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Neural network with Blue filter'],['Cartoon filter']
    ])

def remembering_user_choose(update, context):
    text = update.message.text
    if text == 'Neural network with Blue filter':
        context.user_data['filter_type'] = 'Neural network with Blue filter'
    elif text == 'Cartoon filter':
         context.user_data['filter_type'] = 'Cartoon filter'


#Приветствуем пользователя
def greet_user(update, context):
    text = 'Hello, dear user.\nHere you can cartoonizer your photo using our bot\nPlease choose, how do you want to cartoonize your photo'
    update.message.reply_text(
        text,
        reply_markup = main_keyboard()
    )

#эта функция, которая будет вызывать другие функции, которые будут изменять фотографии изера
def cartoonify(update, context):
    #получаем фото в самом хорошем качестве
    photo = context.bot.getFile(update.message.photo[-1].file_id)
    chat_id = update.effective_chat.id
    # Сохраняем фото с названием photo.jpg в папку downloads
    # меняем фотку с помощью нейросетки
    if context.user_data['filter_type'] == 'Neural network with Blue filter':
       update.message.reply_text('Please, wait a second')
       user_cartoonize_image = cartoonize_using_network(photo)
       #send the image
       update.message.reply_text('Here we go')
       context.bot.send_photo(chat_id=chat_id, photo=user_cartoonize_image)
    #   меняем фотку с помощью фильра, над которым сейчас работает наташа
    elif context.user_data['filter_type'] == 'Cartoon filter':
        # Сохраняем фото с названием photo.jpg в папку downloads
        os.makedirs("downloads", exist_ok=True)
        file_name = os.path.join("downloads", "photo.jpg")
        photo.download(file_name)
        update.message.reply_text("The photo is saved")
        cartoonise_using_cartoonfilter(update, context, file_name)
        
        
    #это пока не работает, пока не знаю почему
    else:
        update.message.reply_text("Please choose, what do you want to use to change your photo")

#функция для фильтров
def cartoonise_using_cartoonfilter(update, context, file_name):
    update.message.reply_text("Processing the photo")
    # Сохраняем обработанное фото под именем cartoon_photo.jpg в папку downloads. 
    # Используется полное имя
    cartoon_file_name = os.path.abspath(os.path.join("downloads", "cartoon_photo.jpg"))

    # Если модуль apply_cartoon_filter выдал ошибку, то отправляем пользователю сообщение.
    try:
        apply_cartoon_filter(os.path.abspath(file_name), cartoon_file_name)
    except TypeError:
        update.message.reply_text("I can't process this photo. Choose another one")
    else:
        # Вывод обработанного фото пользователю, если модуль отработал без ошибок.
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id=chat_id, photo=open(cartoon_file_name, 'rb'))
    
def cartoonize_using_network(photo):
       #get url from image and convert it to bytes   
       url = photo['file_path']
       request_image = requests.get(url)
       request_image.raw.decode_content = True
       user_image_in_bytes = request_image.content
       # convert bytes to nampy array
       numpy_array_format = np.fromstring(user_image_in_bytes, np.uint8)
       image_in_numpy_format = cv2.imdecode(numpy_array_format, cv2.IMREAD_COLOR)
       # cartoonize te image
       cartoonize_image_in_nympy_array = cartoonize.cartoonize_photo(image_in_numpy_format)
       # chande numpy array to image format
       cartoonize_image_in_image_format = Image.fromarray(cartoonize_image_in_nympy_array)
       # change image format to bytes
       image_in_bytes_format = io.BytesIO()
       cartoonize_image_in_image_format.save(image_in_bytes_format, format='JPEG')
       image_in_bytes_format = image_in_bytes_format.getvalue()
       # load bytes into ram, so bot can send it
       user_cartoonize_image = io.BytesIO(image_in_bytes_format)
       return user_cartoonize_image

