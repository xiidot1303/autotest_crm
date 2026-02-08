from django.urls import path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)
from app.views import (
    student, course, teacher, group, lesson, 
    main, payment, accounter, finance, user,
    botwebhook

)

from config import BOT_API_TOKEN

urlpatterns = [
    # login
    path('accounts/login/', LoginView.as_view()),
    path('changepassword/', PasswordChangeView.as_view(
        template_name = 'registration/change_password.html'), name='editpassword'),
    path('changepassword/done/', PasswordChangeDoneView.as_view(
        template_name = 'registration/afterchanging.html'), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # main
    path('', main.main_menu, name='main_menu'),
    path('change-lang/<int:lang>/', main.change_lang, name='change_lang'),
    path('web', main.web_app, name='web_app'),

    # bot
    path(BOT_API_TOKEN, botwebhook.bot_webhook),

    # student
    path('students/list', student.student_list_all, name='student_list_all'),
    path('students/page/<int:pk>/', student.student_page, name='student_page'),
    path('student/edit/<int:pk>/', student.StudentEditView.as_view(), name='student_update'),
    path('student/create', student.StudentCreateView.as_view(), name='student_create'),
    path('student/delete/<int:pk>/', student.student_delete, name='student_delete'),

    # course
    path('course/list', course.course_list_all, name='course_list_all'),
    path('course/create', course.CourseCreateView.as_view(), name='course_create'),
    path('course/edit/<int:pk>/', course.CourseEditView.as_view(), name='course_update'),
    path('course/delete/<int:pk>/', course.course_delete, name='course_delete'),

    # teacher
    path('teachers/list', teacher.teacher_list_all, name='teacher_list_all'),
    path('teacher/edit/<int:pk>/', teacher.TeacherEditView.as_view(), name='teacher_update'),
    path('teacher/create', teacher.TeacherCreateView.as_view(), name='teacher_create'),
    path('teacher/delete/<int:pk>/', teacher.teacher_delete, name='teacher_delete'),

    # group
    path('groups/list', group.group_list_all, name='group_list_all'),
    path('groups/page/<int:pk>/', group.group_page, name='group_page'),
    path('groups/page/<int:pk>/<int:month>/<int:year>/', group.group_page),
    path('group/edit/<int:pk>/', group.GroupEditView.as_view(), name='group_update'),
    path('group/create', group.GroupCreateView.as_view(), name='group_create'),
    path('group/set-student-to-new-group', group.group_set_student_to_new_group, name='group_set_student_to_new_group'),
    path('group/delete/<int:pk>/', group.group_delete, name='group_delete'),
    path('group/remove/student/<int:group_pk>/<int:member_pk>/', group.group_remove_student, name='group_remove_student'),
    path('group/pay', group.group_pay, name='group_pay'),

    # lesson
    path('lesson/page', lesson.lesson_current, name='lesson_page'),
    path('lesson/list', lesson.lesson_page, name='lesson_page'),
    path('lesson/end/<int:pk>/', lesson.lesson_end, name='lesson_end'),
    path('lesson/start/<int:pk>/', lesson.lesson_start, name='lesson_start'),
        # attendance
    path('attendance/change/<int:pk>/<int:status>/', lesson.attendance_change, name='attendance_change'),

    # payment
    path('payment/list/by-student/<int:student_pk>/', payment.payment_list_by_student, name='payment_list_by_student'),
    path('payment/list/by-student/<int:student_pk>/<int:group_pk>/', payment.payment_list_by_student, name='payment_list_by_student'),
    path('payment/pay', payment.payment_pay, name='payment_pay'),
    path('payment/cancel/<int:pk>/', payment.payment_cancel, name='payment_cancel'),

    # accounter
    path('accounter/page', accounter.accounter_page, name='accounter_page'),
    path('accounter/confirm-income/<int:pk>/', accounter.accounter_confirm_income, name='accounter_confirm_income'),
    path('accounter/confirm-incoms-all', accounter.accounter_confirm_incomes_all, name='accounter_confirm_income_all'),
    path('accounter/reject-income/<int:pk>/', accounter.accounter_reject_income, name='accounter_reject_income'),

    # finance 
    path('finance/incomes', finance.finance_incomes, name='finance_incomes'),
    path('finance/debtors', finance.finance_debtors, name='finance_debtors'),

    # user
    path('user/list', user.user_list, name='user_list'),
    path('user/create', user.user_create, name='user_create'),
    path('user/edit/<int:pk>/', user.user_update, name='user_update'),
    path('user/delete/<int:pk>/', user.user_delete, name='user_delete'),
    

]   
