import os
#я не знаю что из этого нужно в этом модуле, а что нет, поэтому беру все
from telegram.ext import Updater, CommandHandler, MessageHandler
from utilitis import main_keyboard

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
    # меняем фотку с помощью нейросетки
    if context.user_data['filter_type'] == 'Neural network':
       cartoonize_using_neuro()
       update.message.reply_text('It\'s working!')
    #меняем фотку с помощью фильра, над которым сейчас работает наташа 
    elif context.user_data['filter_type'] == 'Cartoon filter':
        cartoonise_using_cartoonfilter()
        update.message.reply_text('It\'s working!22')
    #это пока не работает, пока не знаю почему
    else:
        print(33)
        update.message.reply_text("Please choose, what do you want to use to change your photo")
        
        
#функция, куда нужно будет добавить ссылку на нейросеть
def cartoonize_using_neuro():
    print(1)

#функция для фильтров
def cartoonise_using_cartoonfilter():
    print(2)

