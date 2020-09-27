import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)


PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn', 
        'password': 'python'
    }
}
#Приветствуем пользователя
def greet_user(update, context):
    text = 'Hello, dear user.\nHere you can cartoonizer your photo using our bot\nPlease choose, how do you want to cartoonize your photo'
    update.message.reply_text(text,
                              reply_markup = main_keyboard()
                              )
#Суда будут добавляться кнопки для выбора, как пользователь хочет изменить свою фотку
def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Neuron network'],['Cartoon filter']
    ])
#Это не то костыль, не то фича. Нужно запоминать как пользователь хочет изменить свою фотку, поэтому сохраним его желание в данные 
def remembering_user_choose(update, context):
    text = update.message.text
    print(text)
    if text == 'Neuron network':
        context.user_data['Neuron network'] = 1
        print(context.user_data['Neuron network'])
   
    elif text == 'Cartoon filter':
         context.user_data['Cartoon filter'] = 1
         print(context.user_data['Cartoon filter'])
        
#эта функция, которая будет вызывать другие функции, которые будут изменять фотографии изера
def god_func(update, context):
    #получаем фото в самом хорошем качестве
    photo = update.message.photo[-1]
    # меняем фотку с помощью нейросетки
    if context.user_data['Neuron network'] == 1:
       cartoonize_using_neuro()
    #меняем фотку с помощью фильра, над которым сейчас работает наташа 
    elif context.user_data['Cartoon filter'] == 1:
        cartoonise_using_cartoonfilter()
    #это пока не работает, пока не знаю почему
    else:
        print(33)
        update.message.reply_text("Please choose, what do you want to use to change your photo")
        
        
#функция, куда нужно будет добавить ссылку на нейросеть
def cartoonize_using_neuro():
    pass

#функция для фильтров
def cartoonise_using_cartoonfilter():
    pass

#так скажем основное тело бота. Будьте осторожны с изменениями
def main():
    mybot = Updater("Код от Ботфазера", use_context = True) #request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Neuron network)$'), remembering_user_choose))
    dp.add_handler(MessageHandler(Filters.regex('^(Cartoon filter)$'), remembering_user_choose))
    dp.add_handler(MessageHandler(Filters.photo, god_func))
    
    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()
