import os
#я не знаю что из этого нужно в этом модуле, а что нет, поэтому беру все
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import ReplyKeyboardMarkup

from cartoon_filter import cartoon_filter

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Neural network'],['Cartoon filter']
    ])

def remembering_user_choose(update, context):
    text = update.message.text
    if text == 'Neural network':
        context.user_data['filter_type'] = 'Neural network'
        print(context.user_data['filter_type'])
   
    elif text == 'Cartoon filter':
         context.user_data['filter_type'] = 'Cartoon filter'
         print(context.user_data['filter_type'])


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
    # Сохраняем фото с названием photo.jpg в папку downloads
    os.makedirs("downloads", exist_ok=True)
    file_name = os.path.join("downloads", "photo.jpg")
    photo.download(file_name)
    update.message.reply_text("The photo is saved")
    # меняем фотку с помощью нейросетки
    if context.user_data['filter_type'] == 'Neural network':
       cartoonize_using_neuro()
       update.message.reply_text('It\'s working!')
    #меняем фотку с помощью фильра, над которым сейчас работает наташа 
    elif context.user_data['filter_type'] == 'Cartoon filter':
        cartoonise_using_cartoonfilter(update, context, file_name)
        
    #это пока не работает, пока не знаю почему
    else:
        print(33)
        update.message.reply_text("Please choose, what do you want to use to change your photo")
        
        
#функция, куда нужно будет добавить ссылку на нейросеть
def cartoonize_using_neuro():
    print(1)

#функция для фильтров
def cartoonise_using_cartoonfilter(update, context, file_name):
    update.message.reply_text("Processing the photo")
    
    # Сохраняем обработанное фото под именем cartoon_photo.jpg в папку downloads. 
    # Используется полное имя
    cartoon_file_name = os.path.abspath(os.path.join("downloads", "cartoon_photo.jpg"))

    # Если модуль cartoon_filter выдал ошибку, то отправляем пользователю сообщение.
    if cartoon_filter(os.path.abspath(file_name), cartoon_file_name):
        update.message.reply_text("I can't process this photo. Choose another one")
    else:
        # Вывод обработанного фото пользователю, если модуль отработал без ошибок.
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id=chat_id, photo=open(cartoon_file_name, 'rb'))
    


    

