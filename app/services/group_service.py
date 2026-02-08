from app.models import *
from app.services import *
from app.services.payment_service import (
    calculate_monthly_payment as _calculate_monthly_payment,
    calculate_full_payment as _calculate_full_payment,
    delete_empty_payments_of_member as _delete_empty_payments_of_member
)

def all_groups():
    query = Group.objects.all()
    return query

def get_group_by_pk(pk):
    obj = get_object_or_404(Group, pk=pk)
    return obj

def create_group(title, course: Course, teacher: Teacher = None):
    obj = Group.objects.create(
        title=title,
        teacher=teacher,
        course=course,
        start_date=today(),
    )
    return obj

def check_group_has_lesson(obj):
    lessons = Lesson.objects.filter(group=obj)
    if lessons:
        return True
    else:
        return False

def check_teacher_has_lesson(data, obj):
    teacher, weekdays, start_time, end_time = data.get('teacher'), data.get('weekdays'), data.get('start_time'), data.get('end_time')
    query = Group.objects.filter(
        start_time__lt=end_time, end_time__gt=start_time, teacher=teacher
        ).exclude(
            pk=obj.pk
        )   
    for group in query:
        if group.weekdays.all() & weekdays.all():
            return True
    else:
        return False

def filter_groups_that_today_has_lesson():
    now = datetime_now()
    weekday = now.weekday()
    query = Group.objects.filter(
        weekdays__day = weekday, start_date__lte=today(), status=1
    ).exclude(remaining_lessons=0)
    return query

def add_student_to_group(group: Group, student: Student, payment_method, discount, start_date=today()):
    # start_date = today() if not start_date else start_date
    member, is_created = group.members.get_or_create(student=student)
    
    # activate member if inactive
    if not is_created:
        member.status = 1
        member.date = datetime_now()
        member.save()

    group.save()
    if payment_method == 'monthly':
        # calculate monthly payment
        _calculate_monthly_payment(group, student, start_date, discount)
    else:
        _calculate_full_payment(group, student, start_date, discount)

    student.add_student_to_lessons()

def set_student_to_group(group: Group, student: Student, discount, payment_method='full', start_date=today()):
    # start_date = today() if not start_date else start_date
    member = Group_member.objects.create(student=student)
    group.members.add(member)

    group.member = member
    group.save()
    _calculate_full_payment(group, student, start_date, discount)


def get_group_by_payment(payment):
    member = Group_member.objects.filter(payments=payment).first()
    group = Group.objects.get(member=member)
    return group


# GROUP MEMBERS

def create_group_member(student):
    obj = Group_member.objects.create(student=student)
    return obj

def get_group_member_by_pk(pk):
    obj = get_object_or_404(Group_member, pk=pk)
    return obj

def delete_group_member(member=None, member_pk=None):
    member = get_group_member_by_pk(member_pk) if not member else member    
    # member.delete()
    member.status = None
    member.save()

    _delete_empty_payments_of_member(member)

def filter_group_members_by_student(student):
    query = Group_member.objects.filter(student=student).exclude(status=None)
    return query