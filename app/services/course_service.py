from app.models import Course
from app.services import *

def all_courses():
    query = Course.objects.all()
    return query

def get_course_by_pk(pk):
    obj = get_object_or_404(Course, pk=pk)
    return obj
