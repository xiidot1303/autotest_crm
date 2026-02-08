from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.conf import settings
from app.services.teacher_service import *
from app.services.lesson_service import *
from app.services.user_service import is_user_in_group as _is_user_in_group, is_superuser as _is_superuser
from app.services.student_service import get_student_by_user as _get_student_by_user

def go_to_login(request):
    path = request.get_full_path()
    return redirect_to_login(path)

def group_required(*groups):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if _is_user_in_group(request, *groups):
                return function(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator

def group_forbid(*groups):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if not _is_user_in_group(request, *groups) or _is_superuser(request):
                return function(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator

def check_lesson_teacher_is_user(action):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            teacher = get_teacher_by_user(request.user)
            if action == 'lesson_end':
                pk = kwargs['pk']
                lesson = get_lesson_by_id(pk)
            elif action == 'attendance_change':
                pk = kwargs['pk']
                lesson = get_lesson_by_journal(journal_id=pk)

            if lesson.group.teacher == teacher and lesson.start_datetime != None and lesson.end_datetime == None:
                return function(request, *args, **kwargs)

            return go_to_login(request)
        return wrapper
    return decorator

def check_student_is_user():
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if _is_user_in_group(request, 'student') and not _is_superuser(request):
                student_pk = kwargs['student_pk']
                user_student = _get_student_by_user(request.user)
                if user_student.pk != student_pk:
                    return go_to_login(request)

            return function(request, *args, **kwargs)
        return wrapper
    return decorator