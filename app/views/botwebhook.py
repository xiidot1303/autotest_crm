from django.http import HttpResponse
from telegram import Update
from app.bot.update import dp, updater
import json
from django.views.decorators.csrf import csrf_exempt
from config import DEBUG


@csrf_exempt
def bot_webhook(request):

    if DEBUG:
        updater.start_polling()
    else:
        update = Update.de_json(json.loads(request.body.decode("utf-8")), dp.bot)
        dp.update_persistence(update)
        dp.process_update(update)

    return HttpResponse("Bot started!")

