import os
import sys
import logging

from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, ParseMode


import requests
import re

from get_news import headline
from translate import translate_text

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

MODE = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")



if mode == "dev":
	def run(updater):
		updater.start_polling()
elif mode=="prod":
	def run(updater):
	        PORT = int(os.environ.get("PORT", "8443"))
	        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
	        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
	        updater.start_webhook(listen="0.0.0.0",
	                              port=PORT,
	                              url_path=TOKEN)
	        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
	logger.error("No MODE sepcified!")
	sys.exit(1)

def start_handler(update: Update, context: CallbackContext):
    # Creating a handler-function for /start command 
    logger.info("User {} started bot".format(update.effective_user["id"]))
    context.bot.update.message.reply_text("Hello from Python!\nPress /random to get random number")


def news(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id
	contents = headline()
	for news_index in range(10):
		post_news_title = contents['value'][news_index]['name']
		post_news_url = contents['value'][news_index]['url']
		post_news_desc = contents['value'][news_index]['description']

		
		# translate
		# post_news_desc = translate_text(text=post_news_desc, project_id='data-mining-275114')

		# aggregate into message


		message = '<b>'+ post_news_title + '</b> 簡介：' + '<i>' + post_news_desc + '</i> <a href="' + post_news_url + '">連結</a>.'
		context.bot.send_message(chat_id=chat_id, 
                 text= message, 
                 parse_mode=ParseMode.HTML)




if __name__ == '__main__':
	logger.info("Starting Bot")
	updater = Updater(TOKEN, use_context=True)
	
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('start', start_handler))
	dp.add_handler(CommandHandler('news', news))

	run(updater)



