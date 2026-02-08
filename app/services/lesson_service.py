from app.models import Lesson, Journal, Group
from app.services import *

def create_lesson(group):
    members = group.members.filter(status=1)

    lesson = Lesson.objects.create(group=group)
        
    for member in members:
        lesson.journal.create(student=member.student)
        lesson.save()
    
    # minus one lesson in groups
    # group.remaining_lessons -= 1
    group.save()

    return lesson

def start_lesson(lesson):
    lesson.start_datetime = datetime_now()
    lesson.save()

def get_lesson_by_id(id):
    obj = Lesson.objects.get(pk=id)
    return obj

def get_current_lesson(teacher):
    query = Lesson.objects.filter(
        group__teacher=teacher, end_datetime=None
        ).exclude(
            start_datetime = None
        ).order_by('start_datetime')
    return query[0] if query else None

def get_all_active_lessons():
    query = Lesson.objects.filter(group__remaining_lessons__gt=0)
    return query

def get_upcoming_lesson(teacher):
    query = Lesson.objects.filter(
        group__teacher=teacher, start_datetime=None
        )

    return query[0] if query else None

def filter_not_started_lessons():
    query = Lesson.objects.filter(start_datetime=None)
    return query

def get_first_lesson_date_of_student(student, group):
    query = Lesson.objects.filter(group=group, journal__student=student)
    return query[0].start_datetime

def get_lesson_by_journal(journal=None, journal_id=None):
    journal = get_journal_by_id(journal_id) if not journal else None
    obj = Lesson.objects.get(journal__pk=journal.pk)
    return obj

def filter_lessons_by_group(group):
    query = Lesson.objects.filter(
        group = group
        )
    return query

def get_distinct_dates_of_lessons(group):
    dates = Lesson.objects.filter(group=group).exclude(end_datetime=None).values_list(
        'start_datetime__month', 'start_datetime__year'
        ).distinct()
    return dates

def filter_lessons_monthly(group, month, year):
    query = Lesson.objects.filter(
        group = group,
        start_datetime__month = month,
        start_datetime__year = year
        )
    return query

# JOURNAL

def get_journal_by_id(id):
    obj = get_object_or_404(Journal, pk=id)
    return obj

def change_attend_by_id(id, status):
    journal = get_journal_by_id(id)
    journal.attended = status
    journal.save()
    return journal
    
def create_lessons(group: Group):
    for i in range(group.course.lessons):
        create_lesson(group)