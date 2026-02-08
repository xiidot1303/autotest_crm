from app.models import Teacher
from app.services import *

def all_teachers():
    query = Teacher.objects.all()
    return query

def get_teacher_by_pk(pk):
    obj = get_object_or_404(Teacher, pk=pk)
    return obj

def get_teacher_by_user(user):
    obj = get_object_or_404(Teacher, user=user)
    return obj