from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler

#Суда будут добавляться кнопки для выбора, как пользователь хочет изменить свою фотку
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
