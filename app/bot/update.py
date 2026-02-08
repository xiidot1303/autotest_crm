from telegram import Bot
from telegram.ext import Dispatcher, PicklePersistence
from telegram.ext import Updater
from app.bot.handlers import login_handler
from config import BOT_API_TOKEN, DEBUG


persistence = PicklePersistence(filename="persistencebot")

bot_obj = Bot(BOT_API_TOKEN)

if not DEBUG:  # in production
    updater = 1213
    dp = Dispatcher(bot_obj, None, workers=10, use_context=True, persistence=persistence)

else:  # in development
    updater = Updater(
        token=BOT_API_TOKEN, workers=10, use_context=True, persistence=persistence,
    )
    dp = updater.dispatcher




dp.add_handler(login_handler)
