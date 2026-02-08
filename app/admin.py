from django.contrib import admin
from app.models import *
from app.forms import *

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['user_ip', 'lang']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone', 'age']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'lessons']

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'phone']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'remaining_lessons', 'start_time', 'end_time']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['group', 'start_datetime', 'end_datetime']

class JournalAdmin(admin.ModelAdmin):
    list_display = ['student']

class Group_memberAdmin(admin.ModelAdmin):
    list_display = ['student']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['amount', 'due_date', 'payed', 'payed_datetime']

class IncomeAdmin(admin.ModelAdmin):
    list_display = ['amount', 'datetime', 'type', 'conf']

class Bot_userAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'phone', 'lang', 'date']

admin.site.register(Language, LanguageAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Group_member, Group_memberAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Bot_user, Bot_userAdmin)
