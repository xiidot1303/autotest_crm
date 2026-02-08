from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InputMediaPhoto,
    InputMedia,
    ReplyKeyboardRemove,
    Bot,
    ParseMode,
    ChatAction
)
from telegram.ext import (
    ConversationHandler
)
from uuid import uuid4
from config import BOT_API_TOKEN

bot = Bot(BOT_API_TOKEN)


def update_message_reply_text(update, text, reply_markup=None):
    message = update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode = ParseMode.HTML
    )
    return message

def bot_send_message(update, context, text, reply_markup=None):
    bot = context.bot
    message = bot.send_message(
        update.message.chat.id, 
        text,
        reply_markup=reply_markup,
        parse_mode = ParseMode.HTML
        )
    return message

def send_newsletter(bot, chat_id, text, reply_markup=None, pin_message=False):
    try:
    # if True:
        message = bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        if pin_message:
            bot.pin_chat_message(chat_id=chat_id, message_id=message.message_id)
    except:
        w=0

def bot_delete_message(update, context, message_id=None):
    if not message_id:
        message_id = update.message.message_id
    bot = context.bot
    try:
        bot.delete_message(update.message.chat.id, message_id)
    except:
        return

def bot_edit_message_text(update, context, text, msg_id=None):
    bot = context.bot
    if not msg_id:
        msg_id = update.message.message_id
    bot.edit_message_text(
        chat_id=update.message.chat.id,
        message_id=msg_id,
        text=text, 
        parse_mode=ParseMode.HTML
    )


def reply_keyboard_markup(keyboard=[], resize_keyboard=True, one_time_keyboard=False):
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard
    )
    return markup

def reply_keyboard_remove():
    markup = ReplyKeyboardRemove(True)
    return markup


def inlinequeryresultarticle(title, description=None, product_id=None):
    message_content = title
    if product_id:
        message_content = '{}<>?{}'.format(title, product_id)

    article = InlineQueryResultArticle(
        id=str(uuid4()),
        title=title,
        description = description,
        input_message_content=InputTextMessageContent(message_content),
    )
    return article

def update_inline_query_answer(update, article):
    update.inline_query.answer(article, auto_pagination=True)

def bot_answer_callback_query(update, context, text, show_alert=True):
    bot = context.bot
    bot.answer_callback_query(callback_query_id=update.id, text=text, show_alert=show_alert)

def bot_send_chat_action(update, context, chat_action=ChatAction.TYPING):
    bot = context.bot
    bot.sendChatAction(update.message.chat.id, chat_action)

def send_media_group(bot, chat_id, photos):

    all = [InputMediaPhoto(photo.file) for photo in photos.all()]
    try:
        bot.send_media_group(chat_id = chat_id, media = all)
    except:
        w=0