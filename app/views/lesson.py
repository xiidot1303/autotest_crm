from app.views import *
from app.services.lesson_service import *
from app.services.teacher_service import *
from app.services.group_service import *
from app.services.student_service import *
from app.services.course_service import *

@login_required
@group_required('teacher')
def lesson_current(request):
    user = request.user
    teacher = get_teacher_by_user(user)
    lesson = get_current_lesson(teacher)
    upcoming_lesson = get_upcoming_lesson(teacher) if not lesson else None
    journal = lesson.journal.all() if lesson else None
    context = {'journal': journal, 'lesson': lesson, 'upcoming_lesson': upcoming_lesson}
    return render(request, 'lesson/lesson_page.html', context)


@login_required
@permission_required('app.view_lesson')
def lesson_page(request: HttpRequest):
    user = request.user
    groups = all_groups().order_by('-pk')
    students = filter_students_active()
    teachers = all_teachers()
    courses = all_courses()
    student_form = Setting_student_to_groupForm()
    student_form.fields['student'].choices = [(s.pk, s.name) for s in students]
    student_form.fields['teacher'].choices = [(t.pk, t.name) for t in teachers]
    student_form.fields['course'].choices = [(c.pk, c.title) for c in courses]
    context = {'groups': groups, 'student_form': student_form}
    return render(request, 'lesson/lesson_list_active.html', context)


@login_required
@permission_required('app.start_lesson')
# @check_lesson_teacher_is_user('lesson_end')
def lesson_start(request, pk):
    lesson = get_lesson_by_id(pk)
    # start lesson 
    lesson.start_datetime = datetime_now()
    lesson.save()
    # redirect to previous page
    return redirect_back(request)


@login_required
@permission_required('app.end_lesson')
# @check_lesson_teacher_is_user('lesson_end')
def lesson_end(request, pk):
    lesson = get_lesson_by_id(pk)
    # end lesson 
    lesson.end_datetime = datetime_now()
    lesson.save()
    group: Group = lesson.group
    group.remaining_lessons -= 1
    group.save()
    # redirect to previous page
    return redirect_back(request)


# ATTENDANCE
@login_required
@group_required('teacher')
@check_lesson_teacher_is_user('attendance_change')
def attendance_change(request, pk, status):
    status = True if status == 1 else (False if status == 0 else None)
    change_attend_by_id(pk, status)
    return redirect(lesson_current)
