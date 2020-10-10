import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import greet_user, cartoonify,main_keyboard, remembering_user_choose
from settings import BOT_TOKEN, PROXY

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)

#так скажем основное тело бота. Будьте осторожны с изменениями
def main():
    mybot = Updater(BOT_TOKEN, use_context = True) #request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Neural network with Blue filter)$'), remembering_user_choose))
    dp.add_handler(MessageHandler(Filters.regex('^(Cartoon filter)$'), remembering_user_choose))
    dp.add_handler(MessageHandler(Filters.regex('^(Neural network without filters)$'), remembering_user_choose))
    dp.add_handler(MessageHandler(Filters.photo, cartoonify))
    
    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()
