from app.models import Student
from app.services import *
from django.db.models import Exists, OuterRef
from django.contrib.auth.models import Group as Model_group
from app.services.user_service import create_or_update_user as _create_or_update_user

def all_students():
    query = Student.objects.all()
    return query

def get_student_by_pk(pk):
    obj = get_object_or_404(Student, pk=pk)
    return obj

def get_student_by_user(user):
    student = get_object_or_404(Student, user=user)
    return student

def filter_students_who_are_not_in_group(group):
    students = Student.objects.filter(
        ~Exists(group.members.filter(student_id=OuterRef('pk')).exclude(status=None)), 
        status=1
        )
    return students

def filter_students_active():
    students = Student.objects.filter(
        status=1
    )
    return students

def filter_students_who_are_member_of_group(group):
    students = Student.objects.filter(
        Exists(group.members.filter(student_id=OuterRef('pk')).exclude(status=None)), 
        status=1
        )
    return students

def create_or_update_student_user(obj):
    groups = Model_group.objects.filter(name='student').values_list('pk', flat=True)
    user = _create_or_update_user(
        obj.user,
        obj.phone,
        obj.name,
        '.',
        groups,
        '',
        obj.password
    )
    obj.user = user
    obj.save()
    return user

def check_phone_available(phone, obj):
    query = Student.objects.filter(phone=phone).exclude(pk=obj.pk)
    return query
