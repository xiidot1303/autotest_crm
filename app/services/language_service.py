from app.models import Language

def get_language_by_ip(ip):
    return Language.objects.get(user_ip=ip)

def get_lang_by_ip(ip):
    lang_tuple = Language.objects.get_or_create(user_ip=ip)
    lang_obj = lang_tuple[0]
    if lang_tuple[1]:
        lang_obj.lang = 1
        lang_obj.save()
    return lang_obj.lang

def update_lang_by_ip(ip, lang: int):
    lang_obj = get_language_by_ip(ip)
    lang_obj.lang = lang
    lang_obj.save()
    return lang_obj