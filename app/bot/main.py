from app.bot import *
from telegram import WebAppInfo, InlineQueryResult


def start(update, context):
    update_message_reply_text(
        update, 
        'hello', 
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                text = 'Web app',
                web_app = WebAppInfo(url = 'http://127.0.0.1:8000')
            )]]
        )
    )
