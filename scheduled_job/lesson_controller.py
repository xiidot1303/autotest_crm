from app.services.lesson_service import *
from app.services.group_service import *
from app.utils import datetime_now, time_now

def job_create_lesson():
    for group in filter_groups_that_today_has_lesson():
        lesson = create_lesson(group)

def job_start_lesson():
    for lesson in filter_not_started_lessons():
        now = time_now()
        start_time = lesson.group.start_time
        if start_time <= now:
            # start lesson
            start_lesson(lesson)

