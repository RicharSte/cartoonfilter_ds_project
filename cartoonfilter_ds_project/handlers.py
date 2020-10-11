from cartoonize import cartoonize_photo
from cartoon_filter import apply_cartoon_filter
import cv2
import io
import numpy as np
import os
from PIL import Image
import requests
import shutil
from skimage import io as stikIO
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import ReplyKeyboardMarkup, utils
import urllib.request as ur


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Neural network with Blue filter'],['Neural network without filters'],
        ['Cartoon filter']
    ])

def remembering_user_choose(update, context):
    text = update.message.text
    if text == 'Neural network with Blue filter':
        context.user_data['filter_type'] = 'Neural network with Blue filter'
    elif text == 'Cartoon filter':
         context.user_data['filter_type'] = 'Cartoon filter'
    elif text == 'Neural network without filters':
         context.user_data['filter_type'] = 'Neural network without filters'

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
    # меняем фотку с помощью нейросетки
    if context.user_data['filter_type'] == 'Neural network with Blue filter':
       update.message.reply_text('Please, wait a second')
       user_cartoonize_image = cartoonize_using_network_Blue(photo)
       #send the image
       update.message.reply_text('Here we go')
       context.bot.send_photo(chat_id=chat_id, photo=user_cartoonize_image)
    #   меняем фотку с помощью фильра
    elif context.user_data['filter_type'] == 'Cartoon filter':
        update.message.reply_text('Please, wait a second')
        user_cartoonize_image = cartoonise_using_cartoonfilter(photo)
        #send the image
        update.message.reply_text('Here we go')
        context.bot.send_photo(chat_id=chat_id, photo=user_cartoonize_image)
    elif context.user_data['filter_type'] == 'Neural network without filters':
        update.message.reply_text('Please, wait a second')
        user_cartoonize_image = cartoonize_using_network_without_filters(photo)
        #send the image
        update.message.reply_text('Here we go')
        context.bot.send_photo(chat_id=chat_id, photo=user_cartoonize_image)
    else:
        print("Something wrong, i can feel it")

#меняем изображения с помощью фильтров
def cartoonise_using_cartoonfilter(photo):
    #get url
    url = photo['file_path']
    #read bytes from url
    image = stikIO.imread(url) 
    cartoonize_image_in_nympy_array = apply_cartoon_filter(image)
    # chande numpy array to image format
    cartoonize_image_in_image_format = Image.fromarray(cartoonize_image_in_nympy_array)
    # change image format to bytes
    image_in_bytes_format = io.BytesIO()
    cartoonize_image_in_image_format.save(image_in_bytes_format, format='JPEG')
    image_in_bytes_format = image_in_bytes_format.getvalue()
    # load bytes into ram, so bot can send it
    user_cartoonize_image = io.BytesIO(image_in_bytes_format)
    return user_cartoonize_image

# меняем картинку с помощью нейро сети + синий фильтр
def cartoonize_using_network_Blue(photo):
    #get url from image and convert it to bytes   
    url = photo['file_path']
    request_image = requests.get(url)
    request_image.raw.decode_content = True
    user_image_in_bytes = request_image.content
    # convert bytes to nampy array
    numpy_array_format = np.fromstring(user_image_in_bytes, np.uint8)
    image_in_numpy_format = cv2.imdecode(numpy_array_format, cv2.IMREAD_COLOR)
    # cartoonize te image
    cartoonize_image_in_nympy_array = cartoonize_photo(image_in_numpy_format)
    # chande numpy array to image format
    cartoonize_image_in_image_format = Image.fromarray(cartoonize_image_in_nympy_array)
    # change image format to bytes
    image_in_bytes_format = io.BytesIO()
    cartoonize_image_in_image_format.save(image_in_bytes_format, format='JPEG')
    image_in_bytes_format = image_in_bytes_format.getvalue()
    # load bytes into ram, so bot can send it
    user_cartoonize_image = io.BytesIO(image_in_bytes_format)
    return user_cartoonize_image

#меняем фото с помощю нейронки но без синего фильра   
def cartoonize_using_network_without_filters(photo):
    #get url
    url = photo['file_path']
    #read bytes from url
    image = stikIO.imread(url)
    cartoonize_image_in_nympy_array = cartoonize_photo(image)
    # chande numpy array to image format
    cartoonize_image_in_image_format = Image.fromarray(cartoonize_image_in_nympy_array)
    # change image format to bytes
    image_in_bytes_format = io.BytesIO()
    cartoonize_image_in_image_format.save(image_in_bytes_format, format='JPEG')
    image_in_bytes_format = image_in_bytes_format.getvalue()
    # load bytes into ram, so bot can send it
    user_cartoonize_image = io.BytesIO(image_in_bytes_format)
    return user_cartoonize_image

