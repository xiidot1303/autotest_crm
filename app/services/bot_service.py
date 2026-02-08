from app.services import *
from app.models import *


def get_word(text, update=None, chat_id=None):
    if not chat_id:
        chat_id = update.message.chat.id

    user = Bot_user.objects.get(user_id=chat_id)
    if user.lang == "uz":
        return lang_dict[text][0]
    else:
        return lang_dict[text][1]

def is_registered(id):
    if Bot_user.objects.filter(user_id=id).exclude(phone=None):
        return True
    else:
        return False

def get_user_by_update(update):
    user = Bot_user.objects.get(user_id=update.message.chat.id)
    return user

def check_username(update):
    user = get_user_by_update(update)

    if user.username != update.message.chat.username:
        user.username = update.message.chat.username
        user.save()
    if user.firstname != update.message.chat.first_name:
        user.firstname = update.message.chat.first_name
        user.save()

def get_or_create(user_id):
    obj = Bot_user.objects.get_or_create(user_id=user_id)
    
def get_object_by_user_id(user_id):
    obj = Bot_user.objects.get(user_id=user_id)
    return obj

def get_object_by_update(update):
    obj = Bot_user.objects.get(user_id=update.message.chat.id)
    return obj
