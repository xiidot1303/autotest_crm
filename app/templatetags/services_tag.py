from django import template
from app.services import (
    lesson_service, student_service, payment_service, group_service, user_service, language_service
)
from app.utils import get_user_ip

register = template.Library()

@register.filter()
def user_in_group(request, groups):
    return user_service.is_user_in_group(request, groups)

@register.filter()
def student_attended_date(student, group):
    lesson_date = lesson_service.get_first_lesson_date_of_student(student, group)
    return lesson_date.strftime("%d.%m.%Y")
    
@register.filter()
def ordered_members_list_of_group(group, request):
    if user_service.is_user_in_group(request, 'student') and not user_service.is_superuser(request):
        student = student_service.get_student_by_user(request.user)
        students = group.members.filter(student=student).exclude(status=None).order_by('-status', 'student__name')
    else:
        students = group.members.filter().exclude(status=None).order_by('-status', 'student__name')
    return students

@register.filter()
def is_student_attended_to_lesson(lesson, student):
    if journal := lesson.journal.filter(student=student):
        return journal[0].attended
    return ''

@register.filter()
def lessons_current_date(group, date):
    lessons = lesson_service.filter_lessons_monthly(group, date[0], date[1])
    return lessons

@register.filter()
def payable_remaining_amount(member):
    return payment_service.get_payable_remaining_amount_of_member(member)

@register.filter()
def payable_due_date(member):
    return payment_service.get_payable_due_date_of_member(member).strftime("%d.%m.%Y")

@register.filter()
def group_title_by_payment(payment):
    return group_service.get_group_by_payment(payment).title

@register.filter()
def payed_amount(payment):
    return payment.payed_amount

@register.filter()
def remaining_amount(payment):
    return payment.remaining_amount

@register.filter()
def payed_percent(payment):
    percent = payment.payed_amount / payment.amount * 100
    return round(percent) + 5 if percent < 4 else round(percent)

@register.filter()
def filter_incomes(payment):
    return payment.incomes.all().exclude(conf=None).order_by('-pk')

@register.filter()
def groups_of_user(user):
    groups = user.groups.all()
    result = ', '.join(groups.values_list('name', flat=True))
    return result

@register.filter()
def user_lang(request):
    ip = get_user_ip(request)
    return language_service.get_lang_by_ip(ip)

@register.filter()
def student_by_request(request):
    user = request
    return student_service.get_student_by_user(user)
