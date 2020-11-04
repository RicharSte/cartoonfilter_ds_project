import requests
from skimage import io as stikIO
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import ReplyKeyboardMarkup, utils
import urllib.request as ur

from filters import cartoonize_using_network_Blue as nb
from filters import cartoonise_using_cartoonfilter as cf
from filters import cartoonize_using_network_without_filters as wf

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
       #get url from image and convert it to bytes   
       url = photo['file_path']
       request_image = requests.get(url)
       request_image.raw.decode_content = True
       user_image_in_bytes = request_image.content
       user_cartoonize_image = nb(user_image_in_bytes)
       #send the image
       update.message.reply_text('Here we go')
       context.bot.send_photo(chat_id=chat_id, photo=user_cartoonize_image)
    #   меняем фотку с помощью фильра
    elif context.user_data['filter_type'] == 'Cartoon filter':
        update.message.reply_text('Please, wait a second')
        #get url
        url = photo['file_path']
        image = stikIO.imread(url)
        try:
            user_cartoonize_image = cf(image)
            #send the image
            update.message.reply_text('Here we go')
            context.bot.send_photo(chat_id=chat_id, photo=user_cartoonize_image)
        except TypeError:
            update.message.reply_text('Извините, я не могу обработать это фото')
    elif context.user_data['filter_type'] == 'Neural network without filters':
        update.message.reply_text('Please, wait a second')
        #get url
        url = photo['file_path']
        image = stikIO.imread(url)
        user_cartoonize_image = wf(image)
        #send the image
        update.message.reply_text('Here we go')
        context.bot.send_photo(chat_id=chat_id, photo=user_cartoonize_image)
    else:
        print("Something wrong, i can feel it")
