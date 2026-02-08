from django import template
from app.utils import *
from app.templatetags.services_tag import payed_percent as _payed_percent

register = template.Library()

@register.filter()
def string(request, text):
    text = text.lower()
    return get_string(text, request)

@register.filter()
def index(l, i):
    return l[i]

@register.filter()
def time(t):
    return t.strftime('%H:%M')

@register.filter()
def number(number):
    return '{:,}'.format(number).replace(',', ' ')

@register.filter()
def is_even_number(number):
    if number != 0 and number%2 == 0:
        return True
    else:
        return False

@register.filter()
def test(f):
    f.data['label'] = 'lalal'
    return f

@register.filter()
def label_string(request, i):
    text = i.data['label']
    i.data['label'] = string(request, text)
    return i

@register.filter()
def length_form(form):
    return len(form.fields)

@register.filter()
def weekdays_as_string(request, group):
    weekdays_text = ''
    for weekday in group.weekdays.all(): 
        weekdays_text += ', ' if weekdays_text else ''
        weekdays_text += get_string(weekday.title(), request)
    return weekdays_text
                    
@register.filter()
def get_month_by_date(request, date):
    month = month_by_index(date[0], request)
    return month

@register.filter()
def is_current_date(dates, date):
    today_ = today()
    if (date[0] < today_.month and date[1] == today_.year) or date[1] < today_.year:
        # is last date
        if date == dates.last():
            return True
    return True if date[0] == today_.month and date[1] == today_.year else False


@register.filter()
def for_pills(date):
    return '{}-{}'.format(date[0], date[1])

@register.filter()
def status_by_percent(payment):
    percent = _payed_percent(payment)
    if percent >= 100:
        return 'success'
    elif percent < 100 and percent >= 75:
        return 'primary'
    elif percent < 75 and percent >= 50:
        return 'info'
    elif percent < 50 and percent >= 25:
        return 'warning'
    else:
        return 'danger'