from app.utils import *

def text_successfully_created(request):
    text = get_string('successfully created', request)  
    return text

def text_successfully_changed(request):
    text = get_string('successfully changed', request)  
    return text

def text_successfully_deleted(request):
    text = get_string('successfully deleted', request)
    return text

def text_can_not_delete_sth(request, sth, bcoz):
    sth = get_string(sth, request)
    bcoz = get_string(bcoz, request)
    text = get_string('can not delete sth', request).format(
        sth=sth, bcoz=bcoz
    )
    return text