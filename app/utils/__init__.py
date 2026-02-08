from app.resources.strings import lang_dict
from app.services import language_service
from datetime import datetime, date, timedelta
import pandas as pd

def get_string(text, request):
    ip = get_user_ip(request)
    lang = language_service.get_lang_by_ip(ip)
    if text in lang_dict:
        string = lang_dict[text][lang]
    else:
        string = text
    return string

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def datetime_now():
    now = datetime.now()
    return now

def time_now():
    now = datetime.now()
    return now.time()

def today():
    today = date.today()
    return today

def month_by_index(index, request):
    month = date(2022, index, 1).strftime("%B").lower()
    text = get_string(month, request)
    return text

def days_of_month_by_weekday(start_date, end_date, weekdays):
    days = [d.strftime('%F') for d in pd.date_range(start_date, end_date) if d.weekday() in weekdays]
    return days

def get_date_last_day_of_month(date):
    next_month = date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

def get_date_next_month_1st_day(date):
    new_date =  (date.replace(day=1)+timedelta(days=32)).replace(day=1)
    return new_date

def make_discount(amount, percent):
    return amount - (amount * percent / 100)